import { getBaseURL, get, post } from "./request";

const HttpManager = {
    query:(question)=> get(`query?question=${question}`,"")
}
export {HttpManager}