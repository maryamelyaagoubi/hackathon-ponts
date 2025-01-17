const promptForm = document.getElementById("prompt-form");
const submitButton = document.getElementById("submit-button");
const questionButton = document.getElementById("question-button");
const messagesContainer = document.getElementById("messages-container");
const fileButton = document.getElementById("file-button");
const formButton = document.getElementById("uploadForm");

// Réglages du bouton upload
const fileInput = document.getElementById('file-u');
const fileNameElement = document.getElementById('file-name');

fileNameElement.textContent = 'Aucun fichier sélectionné'

fileInput.addEventListener('change', (event) => {
  if (event.target.files.length > 0) {
    fileNameElement.textContent = `Fichier sélectionné : ${fileInput.files[0].name}`;
  } else {
    fileNameElement.textContent = 'Aucun fichier sélectionné';
  }
});
//

const appendHumanMessage = (message) => {
  const humanMessageElement = document.createElement("div");
  humanMessageElement.classList.add("message", "message-human");
  humanMessageElement.innerHTML = message;
  messagesContainer.appendChild(humanMessageElement);
};

const appendAIMessage = async (messagePromise) => {
  // Add a loader to the interface
  const loaderElement = document.createElement("div");
  loaderElement.classList.add("message");
  loaderElement.innerHTML =
    "<div class='loader'><div></div><div></div><div></div>";
  messagesContainer.appendChild(loaderElement);

  // Await the answer from the server
  const messageToAppend = await messagePromise();

  // Replace the loader with the answer
  loaderElement.classList.remove("loader");
  loaderElement.innerHTML = messageToAppend;
};

const handlePrompt = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  promptForm.reset();

  let url = "/prompt";
  if (questionButton.dataset.question !== undefined) {
    url = "/answer";
    // add question to form data
    data.append("question", questionButton.dataset.question);
    delete questionButton.dataset.question;
    questionButton.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }

  appendHumanMessage(data.get("prompt"));

  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.answer;
  });
};

promptForm.addEventListener("submit", handlePrompt);

const handleQuestionClick = async (event) => {
  appendAIMessage(async () => {
    const response = await fetch("/question", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;
    questionButton.dataset.question = question;
    questionButton.classList.add("hidden");
    submitButton.innerHTML = "R�pondre � la question";
    return question;
  });
}


questionButton.addEventListener("click", handleQuestionClick);

// Handle file form submission
const handleFileSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  appendAIMessage(async () => {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();
    const question = result.answer;
    formButton.dataset.question = question;
    formButton.classList.add("hidden");
    return question;
  })
}


formButton.addEventListener("submit", handleFileSubmit);
