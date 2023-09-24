const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault();

  const body = new FormData(form);
  body.append("insertAt", new Date().getTime());
  // try로직 시도하다가 에러발생하면 밑에 로직실행되는 문버
  try {
    const res = await fetch("/items", {
      method: "POST",
      body,
    });
    const data = await res.json();
    // 200이 떨어졌을 때 위도우페이지를 루ㅌ트경로로 이동
    if (data === "200") window.location.pathname = "/";
  } catch (e) {
    console.error(e);
  }
};

form.addEventListener("submit", handleSubmitForm);
