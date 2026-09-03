const calculatorBaseUrl = '/api/calculator'

export async function calculate(operation, firstNumber, secondNumber) {
  const query = new URLSearchParams({
    a: String(firstNumber),
    b: String(secondNumber),
  })
  const response = await fetch(`${calculatorBaseUrl}/${operation}?${query}`)
  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.detail || 'The calculator request failed.')
  }

  if (typeof data.result !== 'number') {
    throw new Error('The calculator returned an invalid response.')
  }

  return data.result
}
