
export function errorToParams(err) {
  console.log(err)
  // const statusCode = (err.response && err.reponse.statusCode) || 500
  // const message = (err.response && err.reponse.statusText) || ("" + err)
  return {
    statusCode: 500,
    message: "Oops. It's broken"
  }
}
