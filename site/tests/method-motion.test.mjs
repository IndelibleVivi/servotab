import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const source = fs.readFileSync(
  process.env.MOTION_SOURCE || path.join(directory, "../public/method-motion.js"),
  "utf8",
);
const applied = "Method applied. Fresh evidence closes the loop.";
const baseline = "Tab moves first. Work responds. Evidence settles.";

function createClassList() {
  const values = new Set();
  return {
    add(value) {
      values.add(value);
    },
    remove(value) {
      values.delete(value);
    },
    contains(value) {
      return values.has(value);
    },
    toggle(value) {
      if (values.has(value)) {
        values.delete(value);
        return false;
      }
      values.add(value);
      return true;
    },
  };
}

function fixture({
  reduced = false,
  count = 1,
  missingButton = false,
  missingStatus = false,
} = {}) {
  let now = 0;
  let serial = 0;
  const timers = new Map();
  const cancelledCallbacks = [];
  const motionListeners = [];

  const media = {
    matches: reduced,
    addEventListener(type, listener) {
      assert.equal(type, "change", "motion preference must use the change event");
      motionListeners.push(listener);
    },
  };

  const roots = Array.from({ length: count }, () => {
    const events = {};
    const attributes = {};
    const statusWrites = [];
    let statusText = baseline;
    const button = {
      textContent: "Invoke method",
      setAttribute(name, value) {
        attributes[name] = value;
      },
      addEventListener(type, listener) {
        assert.equal(type, "click", "method control must use the click event");
        events[type] = listener;
      },
    };
    const status = {
      classList: createClassList(),
      get textContent() {
        return statusText;
      },
      set textContent(value) {
        statusText = value;
        statusWrites.push(value);
      },
    };

    return {
      attributes,
      button,
      classList: createClassList(),
      events,
      status,
      statusWrites,
      querySelector(selector) {
        if (selector === "button") return missingButton ? null : button;
        if (selector === ".motion-status") return missingStatus ? null : status;
        assert.fail(`unexpected method-motion selector: ${selector}`);
      },
    };
  });

  const window = {
    matchMedia(query) {
      assert.equal(
        query,
        "(prefers-reduced-motion: reduce)",
        "method motion must use the reduced-motion media query",
      );
      return media;
    },
    setTimeout(callback, delay) {
      const id = serial;
      serial += 1;
      timers.set(id, { callback, due: now + delay });
      return id;
    },
    clearTimeout(id) {
      const job = timers.get(id);
      if (job) cancelledCallbacks.push(job.callback);
      timers.delete(id);
    },
  };

  vm.runInNewContext(source, {
    document: {
      querySelectorAll(selector) {
        assert.equal(
          selector,
          "[data-method-motion]",
          "method motion must bind only to its data-marked roots",
        );
        return roots;
      },
    },
    window,
  });

  return {
    roots,
    timers,
    click(index = 0) {
      roots[index].events.click?.();
    },
    tick(delta) {
      const target = now + delta;
      while (true) {
        const first = [...timers].sort(
          (left, right) => left[1].due - right[1].due || left[0] - right[0],
        )[0];
        if (!first || first[1].due > target) break;
        now = first[1].due;
        timers.delete(first[0]);
        first[1].callback();
      }
      now = target;
    },
    setReduced(value) {
      media.matches = value;
      motionListeners.forEach((listener) => listener({ matches: value }));
    },
    deliverCancelled() {
      cancelledCallbacks.splice(0).forEach((callback) => callback());
    },
  };
}

test("single activation settles the complete UI state after its delay", () => {
  const result = fixture();
  result.click();

  assert.equal(result.roots[0].classList.contains("is-active"), true);
  assert.equal(result.roots[0].attributes["aria-pressed"], "true");
  assert.equal(result.roots[0].button.textContent, "Return to baseline");
  assert.equal(result.roots[0].status.classList.contains("is-switching"), true);

  result.tick(140);
  assert.equal(result.roots[0].status.textContent, applied);
  assert.equal(result.roots[0].status.classList.contains("is-switching"), false);
});

test("rapid second activation is not overwritten by the first timeout", () => {
  const result = fixture();
  result.click();
  result.tick(100);
  result.click();
  result.tick(50);

  assert.equal(result.roots[0].classList.contains("is-active"), false);
  assert.equal(result.roots[0].attributes["aria-pressed"], "false");
  assert.equal(result.roots[0].button.textContent, "Invoke method");
  assert.equal(result.roots[0].status.textContent, baseline);
  assert.equal(result.roots[0].status.classList.contains("is-switching"), true);

  result.tick(90);
  assert.equal(result.roots[0].status.textContent, baseline);
  assert.equal(result.roots[0].status.classList.contains("is-switching"), false);
});

test("multiple activations retain only the current timer, including id zero", () => {
  const result = fixture();
  result.click();
  result.tick(20);
  result.click();
  result.click();

  assert.equal(result.timers.size, 1);
  result.tick(140);
  assert.equal(result.roots[0].status.textContent, applied);
});

test("reduced-motion activation updates immediately without scheduling", () => {
  const result = fixture({ reduced: true });
  result.click();

  assert.equal(result.roots[0].status.textContent, applied);
  assert.equal(result.roots[0].statusWrites.length, 1);
  assert.equal(result.timers.size, 0);
});

test("switching to reduced motion settles pending state and cancels animation", () => {
  const result = fixture();
  result.click();
  result.setReduced(true);

  assert.equal(result.roots[0].status.textContent, applied);
  assert.equal(result.timers.size, 0);
  assert.equal(result.roots[0].status.classList.contains("is-switching"), false);
});

test("an unchanged reduced-motion preference does not rewrite the live region", () => {
  const result = fixture({ reduced: true });
  result.setReduced(true);

  assert.deepEqual(result.roots[0].statusWrites, []);
  assert.equal(result.roots[0].status.textContent, baseline);
});

test("a late cancelled callback cannot overwrite the current state", () => {
  const result = fixture();
  result.click();
  result.tick(50);
  result.setReduced(true);
  result.click();
  result.deliverCancelled();
  result.tick(200);

  assert.equal(result.roots[0].status.textContent, baseline);
  assert.equal(result.roots[0].status.classList.contains("is-switching"), false);
});

test("independent widgets keep independent pending state", () => {
  const result = fixture({ count: 2 });
  result.click(0);
  result.tick(50);
  result.click(1);
  result.click(0);
  result.tick(140);

  assert.equal(result.roots[0].status.textContent, baseline);
  assert.equal(result.roots[1].status.textContent, applied);
});

test("missing optional elements remain safe", () => {
  const missingButtonResult = fixture({ missingButton: true });
  missingButtonResult.tick(200);

  const missingStatusResult = fixture({ missingStatus: true });
  missingStatusResult.click();
  missingStatusResult.setReduced(true);
  assert.equal(missingStatusResult.timers.size, 0);
});
