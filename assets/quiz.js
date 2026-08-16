/* ============================================================
   Retrieval-practice quiz widget. Pairs with quiz.css.

   Markup contract:

     <div class="quiz">
       <p class="q">Question?</p>
       <ul class="options">
         <li data-correct>The right answer</li>
         <li>A wrong answer</li>
       </ul>
       <p class="why">Shown once answered.</p>
     </div>

   Options are shuffled on load, so answer position carries no
   information. Feedback is immediate — the whole point is a tight
   loop. Wrong answers don't lock the question; keep going until
   it's right, which is what makes it practice rather than a test.
   ============================================================ */

(function () {
  "use strict";

  function shuffle(nodes) {
    for (let i = nodes.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      nodes[i].parentNode.insertBefore(nodes[j], nodes[i]);
      [nodes[i], nodes[j]] = [nodes[j], nodes[i]];
    }
  }

  function initQuiz(quiz, onFirstCorrect) {
    const list = quiz.querySelector(".options");
    const why = quiz.querySelector(".why");
    if (why) why.hidden = true;
    if (!list) return;

    shuffle(Array.from(list.children));

    let solved = false;

    Array.from(list.querySelectorAll("li")).forEach((li) => {
      const isCorrect = li.hasAttribute("data-correct");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.innerHTML = li.innerHTML;
      li.innerHTML = "";
      li.appendChild(btn);

      btn.addEventListener("click", () => {
        if (solved) return;

        if (isCorrect) {
          solved = true;
          btn.classList.add("correct");
          list.querySelectorAll("button").forEach((b) => (b.disabled = true));
          if (why) why.hidden = false;
          onFirstCorrect(quiz.dataset.firstTry !== "missed");
        } else {
          // Record the miss before revealing, so the score is honest.
          quiz.dataset.firstTry = "missed";
          btn.classList.add("wrong");
          btn.disabled = true;
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    const quizzes = Array.from(document.querySelectorAll(".quiz"));
    if (!quizzes.length) return;

    let firstTry = 0;
    let done = 0;

    const score = document.querySelector(".quiz-score");
    function render() {
      if (!score) return;
      score.textContent =
        done < quizzes.length
          ? `${done} / ${quizzes.length} answered`
          : `${firstTry} / ${quizzes.length} first try`;
    }

    quizzes.forEach((q) =>
      initQuiz(q, (wasFirstTry) => {
        done++;
        if (wasFirstTry) firstTry++;
        render();
      })
    );

    render();
  });
})();
