import { getContentOfArticle } from "./utils/content-extractor";
import { render } from "./ui/qa";

import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkRehype from "remark-rehype";
import rehypeStringify from "rehype-stringify";

let ua = navigator.userAgent;
let browserName = ua.indexOf("Chrome") > -1 ? "Chrome" : "Firefox";
let CORE = browserName === "Chrome" ? chrome : browser;
let storage = chrome.storage;

async function markdownToHtml(markdown) {
  const file = await unified()
    .use(remarkParse) // Parse Markdown to syntax tree
    .use(remarkRehype) // Convert Markdown syntax tree to HTML syntax tree
    .use(rehypeStringify) // Convert HTML syntax tree to HTML string
    .process(markdown); // Process the input markdown

  return String(file); // Return the processed HTML as a string
}

async function run() {
  // rendering container
  const innerContainerBody = render(CORE, storage);

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

  port.onMessage.addListener(async function (msg) {
    if (msg.answer) {
      innerContainerBody.innerHTML = await markdownToHtml(msg.answer);
    }
  });

  port.postMessage({ content });

  // postproc
  storage.local.set({ uiOpened: true }, function () {
    console.log("Page-Digest Running");
  });
}

run();
