import { ce } from "../utils/helper";
import * as CrossIC from "../../../../assets/res/cross.svg";

export function render(CORE) {
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

  const innerContainerHeading = container.querySelector(
    "#summarize__heading-text"
  );
  innerContainerHeading.innerHTML =
    '<p>Summarized <a href="https://chat.openai.com/chat" target="_blank" class="sumz-text-sm">by ChatGPT</a></p>';

  const innerContainerBody = container.querySelector("#summarize__body");
  innerContainerBody.innerHTML = "<p>Waiting for ChatGPT response...</p>";

  // const closeButton = container.querySelector("#summarize__close-button");
  // closeButton.addEventListener("click", function () {
  //   document.body.removeChild(root);
  // });

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
      font-size: 16px;
    }
  `;
  doc.appendChild(style);
}

function createContainer() {
  return ce({
    tag: "div",
    props: { className: "summarize-gpt-container" },
    children: [
      {
        tag: "div",
        props: {
          className:
            "sumz-min-w-[30%] sumz-max-h-[80%] sumz-max-w-[30%] sumz-fixed sumz-right-4 sumz-top-8 sumz-flex sumz-flex-col sumz-items-center sumz-justify-center sumz-rounded-lg sumz-bg-white sumz-shadow-md",
        },
        children: [
          // heading
          {
            tag: "div",
            props: {
              className:
                "sumz-flex sumz-h-[40px] sumz-w-full sumz-items-center sumz-justify-between sumz-rounded-t-lg sumz-bg-gray-200 sumz-px-4",
            },
            children: [
              {
                tag: "div",
                props: {
                  id: "summarize__heading-text",
                  className:
                    "sumz-text-xl sumz-font-black sumz-animate-text sumz-bg-gradient-to-r sumz-from-teal-500 sumz-via-purple-500 sumz-to-orange-500 sumz-bg-clip-text sumz-text-transparent",
                },
              },
              // {
              //   tag: "img",
              //   props: {
              //     id: "summarize__close-button",
              //     className:
              //       "sumz-h-[24px] sumz-w-6 sumz-cursor-pointer sumz-rounded-lg hover:sumz-bg-sky-200",
              //     src: CrossIC,
              //     alt: "close",
              //   },
              // },
            ],
          },
          // divider
          {
            tag: "div",
            props: { className: "sumz-w-full sumz-h-1 sumz-bg-gray-300" },
          },
          // body
          {
            tag: "div",
            props: {
              className:
                "sumz-h-full sumz-w-full sumz-overflow-y-auto sumz-px-4 sumz-py-4",
            },
            children: [
              {
                tag: "div",
                props: {
                  id: "summarize__body",
                  className:
                    "sumz-text-3-xl sumz-mb-2 sumz-flex sumz-flex-col sumz-whitespace-pre-line sumz-text-gray-700",
                },
              },
            ],
          },
          // divider
          {
            tag: "div",
            props: { className: "sumz-w-full sumz-h-1 sumz-bg-gray-200" },
          },
          // footer
          {
            tag: "div",
            props: { className: "sumz-m-2" },
            children: [
              {
                tag: "div",
                props: {
                  className:
                    "sumz-flex sumz-h-[32px] sumz-w-full sumz-items-center sumz-justify-center",
                },
                children: [
                  {
                    tag: "div",
                    props: {
                      className:
                        "sumz-text-lg sumz-font-bold sumz-text-gray-600",
                      innerText: "Help Us",
                    },
                  },
                  {
                    tag: "button",
                    props: {
                      id: "summarize__animation-button",
                      onclick: () =>
                        window.open("https://tally.so/r/woD2eP", "_blank"),
                      className:
                        "sumz-rounded-full sumz-border-2 sumz-border-sky-600 sumz-m-2 sumz-px-1 sumz-py-1 sumz-text-lg sumz-text-sky-600 sumz-transition-colors hover:sumz-bg-sky-100",
                    },
                    children: [
                      {
                        tag: "span",
                        props: {
                          className:
                            "sumz-pointer-events-none sumz-absolute sumz-inset-0 -sumz-z-10 sumz-block",
                          id: "summarize__sparkles-container",
                        },
                      },
                      {
                        tag: "span",
                        props: {
                          className:
                            "sumz-block sumz-h-[16px] sumz-overflow-hidden sumz-z-10",
                          id: "summarize__letters-container",
                        },
                      },
                    ],
                  },
                ],
              },
              {
                tag: "div",
                props: {
                  className: "sumz-text-sm sumz-text-gray-600 sumz-pt-2",
                  innerText:
                    "Share Your Feedback & Ideas for Summarize and Beyond",
                },
              },
            ],
          },
        ],
      },
    ],
  });
}
