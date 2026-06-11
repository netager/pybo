<script>
  // ../lib/api.js 로 fetch 공통화 한 이후에 수정한 내용
  import fastapi from "../lib/api"
  import Error from "../components/Error.svelte"
  import { link, push } from 'svelte-spa-router'
  import { is_login, username } from "../lib/store"
  import { marked } from 'marked'
  import moment from 'moment/min/moment-with-locales'
  moment.locale('ko')

  // 나를 내 부모가 나를 콜했을때의 params 를 가져옴
  // Home.svelte에서 나를 콜했기 때문에 Home.svelte에서 콜한 로직 확인 
  export let params = {}
  let question_id = params.question_id

  // json 값을 받아오기 위해 필수적으로 question 변수 초기화 
  // {answers:[]}으로 변경해야 한다. 
  // 왜냐하면 등록된 답변을 표시하는 each문에서 question.answers를 참조하고 있기 때문이다. 
  // 질문 상세 조회 API는 비동기로 진행되므로 아직 조회가 되지 않은 상태에서 each문이 실행되면 
  // answers 항목이 없어서 오류가 발생한다.
  let question = {answers: [], voter: [], content: ''}
  let content = ""
  let error = {detail: []}

  function get_question() {
    fastapi('get', '/api/question/detail/' + question_id, {}, (json) => {
      question = json
    })
  }

  get_question()

  function post_answer(event) {
    // <form>은 제출하면 기본적으로 페이지를 새로고침하거나 다른 URL로 이동합니다.
    // event.preventDefault() 를 사용하면 이를 하지 않도록 함.
    // 즉, 페이지 새로고침 없이 내가 작성한 JavaScript 코드만 실행
    event.preventDefault()

    let url = "/api/answer/create/" + question_id
    let params = {
      content: content
    }
    fastapi('post', url, params, 
    (json) => {
      content = ''
      error = {detail: []}
      get_question()
    },
    (err_json) => {
      error = err_json 
    })
  }

  // 질문 삭제 
  function delete_question(_question_id) {
    if(window.confirm('정말로 삭제하시겠습니까?')) {
      let url = "/api/question/delete"
      let params = {
        question_id: _question_id
      }
      fastapi('delete', url, params,
        (json) => {
          push('/')
        },
        (err_json) => {
          error = err_json
        }
      )
    }
  }

  // 답변 삭제
  function delete_answer(answer_id) {
    if(window.confirm('정말로 삭제하시겠습니까?')) {
      let url = "/api/answer/delete"
      let params = {
        answer_id: answer_id
      }
      fastapi('delete', url, params,
        (json) => {
          get_question()
        },
        (err_json) => {
          error = err_json
        }
      )
    }
  }

  // 질문 추천하기
  function vote_question(_question_id) {
    if(window.confirm('정말로 추천하시겠습니까?')) {
      let url = "/api/question/vote"
      let params = {
        question_id: _question_id
      }
      fastapi('post', url, params,
        (json) => {
          get_question()
        },
        (err_json) => {
          error = err_json
        }
      )
    }
  }

  // 답변 추천하기
  function vote_answer(answer_id) {
    if(window.confirm("정말로 추천하시겠습니까?")) {
      let url = "/api/answer/vote"
      let params = {
        answer_id: answer_id
      }
      fastapi('post', url, params,
        (json) => {
          get_question()
        },
        (err_json) => {
          error = err_json
        }
      )
    }
  }
</script>

<div class="container my-3">
  <!-- 질문 -->
  <h2 class="border-bottom py-2">{question.subject}</h2>
  <div class="card my-3">
    <div class="card-body">
      <!-- markdown(marked) 적용 -->
      <!-- <div class="card-text" style="white-space: pre-line;">{question.content}</div> -->
      <div class="card-text">
        {@html marked.parse(question.content)}
      </div> 
      <div class="d-flex justify-content-end">
        {#if question.modify_date }
          <div class="badge bg-light text-dark p-2 text-start mx-3">
            <div class="mb-2">modified at</div>
            <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
          </div>
        {/if}
          <div class="badge bg-light text-dark p-2 text-start">
            <div class="mb-2">{ question.user ? question.user.username : ""}</div>
            <div>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
          </div>
      </div>
      <div class="my-3">
        <button class="btn brn-sm btn-outline-secondary" on:click={() => vote_question(question.id)}> 
                      추천
          <span class="badge rounded-pill bg-success">{ question.voter.length }</span>
        </button>
        {#if question.user && $username === question.user.username}
        <a use:link href="/question-modify/{question.id}"
          class="btn brn-sm btn-outline-secondary">수정</a>
        <button class="btn brn-sm btn-outline-secondary"
          on:click={() => delete_question(question.id)}>삭제</button>
        {/if}
      </div>
    </div>
  </div>

  <!-- 목록 조회로 이동 -->
  <button class="btn btn-secondary" on:click={() => {
    push('/')
  }}>목록으로</button>

  <!-- 답변 목록 -->
  <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>
  {#each question.answers as answer}
  <div class="card my-3">
    <div class="card-body">
      <!-- 마크다운(marked) 적용 -->
      <!-- <div class="card-text" style="white-space: pre-line;">{answer.content}</div> -->
      <div class="card-text">
        {@html marked.parse(answer.content)}
      </div>
      <div class="d-flex justify-content-end">
        {#if answer.modify_date}
          <div class="badge bg-light text-dark p-2 text-start mx-3">
            <div class="mb-2">modified at</div>
            <div>{moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
          </div>
        {/if}
        <div class="badge bg-light text-dark p-2 text-start">
          <div class="mb-2">{ answer.user ? answer.user.username : ""}</div>
          <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
        </div>
      </div>
      <div class="my-3">
        <button class="btn btn-sm btn-outline-secondary" 
          on:click={() => vote_answer(answer.id)}>추천
          <span class="badge rounded-pill bg-success">{ answer.voter.length }</span>
        </button>
        {#if answer.user && $username === answer.user.username}
          <a use:link href="/answer-modify/{answer.id}"
            class="btn btn-sm btn-outline-secondary">수정</a>  
          <button class="btn btn-sm btn-outline-secondary"
            on:click={() => delete_answer(answer.id)}>삭제</button>
        {/if}
      </div>
    </div>
  </div>
  {/each}
  <!-- 답변 등록 -->
  <Error error={error} />
  <form method="post" class="my-3">
    <div class="mb-3">
      <textarea rows="10" bind:value={content} class="form-control"></textarea>
    </div>
    <input type="submit" value="답변등록" class="btn btn-primary {$is_login ? '' : 'disabled'}"  on:click="{post_answer}" />
  </form>
</div>
