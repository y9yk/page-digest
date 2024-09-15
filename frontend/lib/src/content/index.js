import { getContentOfArticle } from "./utils/content-extractor";
import { render } from "./ui/qa";

let ua = navigator.userAgent;
let browserName = ua.indexOf("Chrome") > -1 ? "Chrome" : "Firefox";
let CORE = browserName === "Chrome" ? chrome : browser;
let storage = chrome.storage;

async function run() {
  // rendering container
  const innerContainerBody = render(CORE);

  // parsing content of original page
  let content;
  let selection = window.getSelection();
  if (selection.isCollapsed) {
    content = getContentOfArticle();
  } else {
    content = selection.toString();
  }

  // handling message
  const port = CORE.runtime.connect();

  port.onMessage.addListener(function (msg) {
    if (msg.answer) {
      innerContainerBody.innerHTML = msg.answer;
    } else {
      // loading
    }
  });

  port.postMessage({ content });

  // postproc
  storage.local.set({ uiOpened: true }, function () {
    console.log("Page-Digest Running");
  });
}

run();
