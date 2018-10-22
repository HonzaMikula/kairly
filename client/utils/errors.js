
export function errorToParams(err) {
  const statusCode = err.response && err.response.status
  if (statusCode === 404) {
    return { statusCode: 404, message: 'Page not found'}
  }

  console.log(err)
  return {
    statusCode: 500,
    message: "Oops. It's broken"
  }
}
