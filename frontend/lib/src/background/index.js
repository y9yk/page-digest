import ExpiryMap from "expiry-map";
import { fetchSSE } from "./fetch-sse.js";

// // create global vars
let ua = navigator.userAgent;
let browserName = ua.indexOf("Chrome") > -1 ? "Chrome" : "Firefox";
let CORE = browserName === "Chrome" ? chrome : browser;

// // set config and cache
const ENDPOINT_URL = "http://localhost:8000";
const PATH_SUMMARY = "/digest/content";
const CHUNK_SIZE = 3000;
const EXPIRE_TIME = 10 * 1000;
const cache = new ExpiryMap(EXPIRE_TIME);

// functions
function splitTextIntoChunks(text, maxLength) {
  const chunks = [];
  const words = text.split(/\s+/);
  let currentChunk = "";

  for (const word of words) {
    if (currentChunk.length + word.length + 1 <= maxLength) {
      currentChunk += (currentChunk ? " " : "") + word;
    } else {
      chunks.push(currentChunk);
      currentChunk = word;
    }
  }

  if (currentChunk) {
    chunks.push(currentChunk);
  }

  return chunks;
}

function combineSummaries(summaries) {
  let combinedSummary = "";
  for (const summary of summaries) {
    combinedSummary += (combinedSummary ? " " : "") + summary;
  }

  return combinedSummary;
}

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
        console.log("sse message", message);
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
  // Add a badge to signify the extension is in use
  // CORE.action.setBadgeBackgroundColor({ color: [242, 38, 19, 230] });
  // CORE.action.setBadgeText({ text: "GPT" });

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
      const chunk_size = CHUNK_SIZE;
      const text = request.content;

      // split content into chunks
      const chunks = splitTextIntoChunks(text, chunk_size);

      // call summary API
      let summary = "";
      for (const chunk of chunks) {
        await getSummary({
          content: chunk,
          callback: (answer) => {
            summary += answer;
            port.postMessage({
              answer: summary,
            });
          },
        });
      }
    } catch (err) {
      console.error(err);
      port.postMessage({ error: err.message });
    }
  });
});
