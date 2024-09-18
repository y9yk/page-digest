import { ce } from "../utils/helper";

export function render(CORE, storage) {
  // create container
  const container = createContainer();

  let root = document.createElement("div");
  root.id = "summarize-root";
  document.body.appendChild(root);

  let shadowRoot = root.attachShadow({ mode: "open" });
  // Appending the styles to the shadow root
  if (!shadowRoot.querySelector(".summarize-styles"))
    addStylesheet(CORE, shadowRoot, "styles.css", "summarize-styles");
  shadowRoot.appendChild(container);

  // Adding styles to position the root
  root.style.position = "fixed";
  root.style.zIndex = "9999"; // Make sure it's on top of other elements

  // Loading Progress
  const innerContainerBody = container.querySelector("#summarize__body");
  innerContainerBody.innerHTML = `
  <div class="flex justify-center">
    <svg xmlns="http://www.w3.org/2000/svg" style="margin: auto; background: none;" width="40" height="40" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
      <circle cx="50" cy="50" r="32" stroke-width="8" stroke="#3498db" stroke-dasharray="50.26548245743669 50.26548245743669" fill="none" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" keyTimes="0;1" values="0 50 50;360 50 50"></animateTransform>
      </circle>
    </svg>
  </div>`;

  // Close Message Block
  const closeButton = container.querySelector("#summarize__close-button");
  closeButton.addEventListener("click", function () {
    document.body.removeChild(root);
    storage.local.set({ uiOpened: false }, function () {});
  });

  return innerContainerBody;
}

function addStylesheet(CORE, doc, link, classN) {
  const path = CORE.runtime.getURL(link),
    styleLink = document.createElement("link");

  styleLink.setAttribute("rel", "stylesheet");
  styleLink.setAttribute("type", "text/css");
  styleLink.setAttribute("href", path);

  if (classN) styleLink.className = classN;

  doc.appendChild(styleLink);

  const style = document.createElement("style");
  style.textContent = `
    :host {
      all: initial;
    }
    .summarize-gpt-container * {
      font-family: sans-serif;
      line-height: normal;
      font-size: 15px;
    }
    .rounded-t-box {
      border-top-left-radius: 1rem;
      border-top-right-radius: 1rem;
    }
    .rounded-b-box {
      border-bottom-left-radius: 1rem;
      border-bottom-right-radius: 1rem;
    }
    .text-wrap {
      overflow-wrap: break-word;
      word-wrap: break-word;
      hyphens: auto; /* Optional, for better hyphenation */
    }
  `;
  doc.appendChild(style);
}

function createContainer() {
  return ce({
    tag: "div",
    props: {
      className:
        "summarize-gpt-container bg-gray-100 flex items-center justify-center min-h-screen",
    },
    children: [
      // container
      {
        tag: "div",
        props: {
          className:
            "fixed top-2 right-4 w-1/4 bg-white shadow-lg h-[calc(100vh-40px)] my-2 flex flex-col justify-between rounded-t-box rounded-b-box shadow-lg",
        },
        children: [
          // header
          {
            tag: "header",
            props: {
              className:
                "bg-slate-300 flex items-center justify-between px-4 py-4 rounded-t-box",
            },
            children: [
              {
                tag: "div",
                props: {},
                children: [
                  {
                    tag: "h1",
                    props: {
                      className: "text-sm font-bold text-black",
                      innerText: "Page Digest",
                    },
                  },
                  {
                    tag: "h3",
                    props: {
                      className: "text-[12px] text-black",
                      innerText: "Web Page Translator and Summarizer",
                    },
                  },
                ],
              },
              {
                tag: "button",
                props: {
                  id: "summarize__close-button",
                  type: "button",
                  className:
                    "text-[10px] bg-white text-slate-500 px-3 py-1 rounded-t-box rounded-b-box shadow-md hover:bg-slate-500 hover:text-white",
                  innerText: "x",
                },
              },
            ],
          },
          // main
          {
            tag: "article",
            props: {
              id: "summarize__body",
              className:
                "p-4 flex-grow bg-gray-50 overflow-y-auto flex-1 break-words prose prose-slate",
              innerText: "",
            },
          },
          // footer
          {
            tag: "footer",
            props: { className: "bg-slate-300 py-4 text-center rounded-b-box" },
            children: [
              {
                tag: "div",
                props: {},
                children: [
                  {
                    tag: "h1",
                    props: {
                      className: "text-[12px] text-black",
                      innerText: "© 2024. Page Digest. All Rights Reserved.",
                    },
                  },
                ],
              },
            ],
          },
        ],
      },
    ],
  });
}
