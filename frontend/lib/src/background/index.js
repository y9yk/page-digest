import { fetchSSE } from "./fetch-sse.js";

// vars
const ua = navigator.userAgent;
const browserName = ua.indexOf("Chrome") > -1 ? "Chrome" : "Firefox";
const CORE = browserName === "Chrome" ? chrome : browser;
const ENDPOINT_URL = "http://localhost:8000";
const PATH_SUMMARY = "/digest/content";
const CHUNK_SIZE = 3000;

// functions
async function getSummary({
  content,
  content_type,
  model,
  max_tokens,
  callback,
}) {
  const data = {
    content: content || "",
    content_type: content_type || "text",
    model: model || "gpt-4o",
    max_tokens: max_tokens || 2000,
  };

  console.log(data);

  await fetchSSE(`${ENDPOINT_URL}${PATH_SUMMARY}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    onMessage(message) {
      try {
        if (message) {
          callback(message);
        }
      } catch (err) {
        console.log("SSE Message", message);
        console.log(`Error in onMessage: ${err}`);
      }
    },
    onError(err) {
      console.log(`Error in fetchSSE: ${err}`);
    },
  });
}

// main function
function executeScripts(tab) {
  const tabId = tab.id;
  CORE.scripting.executeScript({
    target: { tabId },
    files: ["content.bundle.js"],
  });
}

// Load on clicking the extension icon
CORE.action.onClicked.addListener(async (...args) => {
  executeScripts(...args);
});

// Listen for messages
CORE.runtime.onConnect.addListener((port) => {
  port.onMessage.addListener(async (request, sender, sendResponse) => {
    try {
      // call summary API
      let summary = "";
      await getSummary({
        content: request.content,
        callback: (answer) => {
          summary += answer;
          port.postMessage({
            answer: summary,
          });
        },
      });
    } catch (err) {
      console.error(err);
      port.postMessage({ error: err.message });
    }
  });
});
