<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'

import { calculate } from './services/calculatorApi'

const operations = [
  { value: 'add', label: 'Add', symbol: '+' },
  { value: 'subtract', label: 'Subtract', symbol: '−' },
  { value: 'multiply', label: 'Multiply', symbol: '×' },
  { value: 'divide', label: 'Divide', symbol: '÷' },
]

const firstNumber = ref(0)
const secondNumber = ref(0)
const operation = ref('add')
const result = ref(null)
const errorMessage = ref('')
const isCalculating = ref(false)
const firstNumberInput = ref(null)
let calculationTimer
let calculationRequestId = 0
let suppressAutomaticCalculation = false

function selectOperation(selectedOperation) {
  operation.value = selectedOperation
}

function cancelPendingCalculation() {
  window.clearTimeout(calculationTimer)
  calculationRequestId += 1
  isCalculating.value = false
}

function clearInputs() {
  cancelPendingCalculation()
  firstNumber.value = null
  secondNumber.value = null
  firstNumberInput.value?.focus()
}

function resetCalculator() {
  suppressAutomaticCalculation = true
  cancelPendingCalculation()
  firstNumber.value = 0
  secondNumber.value = 0
  operation.value = 'add'
  result.value = null
  errorMessage.value = ''
  firstNumberInput.value?.focus()
  nextTick(() => {
    suppressAutomaticCalculation = false
  })
}

function inputsAreReady() {
  return (
    firstNumber.value !== null &&
    firstNumber.value !== '' &&
    secondNumber.value !== null &&
    secondNumber.value !== '' &&
    Number.isFinite(Number(firstNumber.value)) &&
    Number.isFinite(Number(secondNumber.value))
  )
}

async function calculateResult(requestId) {
  if (requestId !== calculationRequestId) return

  try {
    const nextResult = await calculate(operation.value, firstNumber.value, secondNumber.value)
    if (requestId === calculationRequestId) {
      result.value = nextResult
    }
  } catch (error) {
    if (requestId === calculationRequestId) {
      result.value = null
      errorMessage.value = error instanceof Error ? error.message : 'The calculation could not be completed.'
    }
  } finally {
    if (requestId === calculationRequestId) {
      isCalculating.value = false
    }
  }
}

function scheduleCalculation() {
  cancelPendingCalculation()

  if (suppressAutomaticCalculation || !inputsAreReady()) return

  const requestId = calculationRequestId
  errorMessage.value = ''
  isCalculating.value = true
  calculationTimer = window.setTimeout(() => calculateResult(requestId), 250)
}

watch([firstNumber, secondNumber, operation], scheduleCalculation, { immediate: true })

onBeforeUnmount(cancelPendingCalculation)
</script>

<template>
  <main class="page-shell">
    <section class="calculator-card" aria-labelledby="calculator-heading">
      <header>
        <p class="eyebrow">IST 402 · Hello Agent</p>
        <div class="title-row">
          <h1 id="calculator-heading">Calculator</h1>
          <span class="version" aria-label="Version 1.1.0">v1.1.0</span>
        </div>
        <p class="introduction">Choose an operation and enter two numbers. The result updates automatically.</p>
      </header>

      <form class="calculator-form" @submit.prevent="scheduleCalculation">
        <div class="number-fields">
          <div class="field">
            <label for="first-number">First number</label>
            <input
              id="first-number"
              ref="firstNumberInput"
              v-model.number="firstNumber"
              type="number"
              step="any"
              required
            />
          </div>

          <div class="field">
            <label for="second-number">Second number</label>
            <input id="second-number" v-model.number="secondNumber" type="number" step="any" required />
          </div>
        </div>

        <fieldset class="operation-picker">
          <legend>Operation</legend>
          <div class="operation-grid">
            <button
              v-for="item in operations"
              :key="item.value"
              class="operation-button"
              :class="{ 'is-selected': operation === item.value }"
              type="button"
              :aria-label="item.label"
              :aria-pressed="operation === item.value"
              @click="selectOperation(item.value)"
              @keydown.enter.prevent="selectOperation(item.value)"
              @keydown.space.prevent="selectOperation(item.value)"
            >
              <span class="operation-symbol" aria-hidden="true">{{ item.symbol }}</span>
              <span>{{ item.label }}</span>
            </button>
          </div>
        </fieldset>

        <div class="form-actions">
          <button class="utility-button" type="button" @click="clearInputs">
            Clear inputs
          </button>
          <button class="utility-button reset-button" type="button" @click="resetCalculator">
            Reset calculator
          </button>
        </div>
      </form>

      <div class="feedback-grid">
        <section
          class="feedback-panel result-panel"
          :class="{ 'is-active': result !== null }"
          :aria-busy="isCalculating"
          aria-labelledby="result-heading"
        >
          <h2 id="result-heading">Result</h2>
          <output aria-live="polite">
            {{ isCalculating ? 'Calculating…' : result === null ? 'No result yet.' : result }}
          </output>
        </section>

        <section
          class="feedback-panel error-panel"
          :class="{ 'is-active': errorMessage }"
          aria-labelledby="error-heading"
        >
          <h2 id="error-heading">Error</h2>
          <p role="alert">{{ errorMessage || 'No errors.' }}</p>
        </section>
      </div>
    </section>
  </main>
</template>

<style scoped>
.page-shell {
  display: grid;
  min-height: 100vh;
  place-items: center;
  padding: clamp(1rem, 4vw, 3.5rem) 1rem;
}

.calculator-card {
  position: relative;
  width: min(100%, 56rem);
  overflow: hidden;
  padding: clamp(1.5rem, 5vw, 3.75rem);
  border: 1px solid #d4c5b5;
  border-radius: 0.5rem 1.5rem 1.5rem 0.5rem;
  background: #fffdf9;
  box-shadow: 0 1.5rem 4rem rgba(68, 48, 28, 0.14);
}

.calculator-card::before {
  position: absolute;
  top: 0;
  bottom: 0;
  left: clamp(0.7rem, 2vw, 1.25rem);
  width: 2px;
  background: rgba(165, 68, 23, 0.3);
  content: '';
}

.eyebrow {
  margin-bottom: 0.35rem;
  color: #9a4313;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.title-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.65rem;
}

h1 {
  color: #2d241d;
  font-size: clamp(2rem, 7vw, 3.25rem);
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 1;
}

.version {
  color: #76685b;
  font-size: 0.8rem;
  font-weight: 400;
  letter-spacing: 0.06em;
}

.introduction {
  max-width: 34rem;
  margin-top: 1rem;
  color: #675b50;
}

.calculator-form {
  display: grid;
  gap: 1.25rem;
  margin-top: 2rem;
}

.number-fields,
.feedback-grid {
  display: grid;
  gap: 1rem;
}

.field {
  display: grid;
  gap: 0.45rem;
}

label,
legend,
h2 {
  color: #3b3027;
  font-size: 0.88rem;
  font-weight: 700;
}

input,
select {
  width: 100%;
  min-height: 3rem;
  padding: 0.7rem 0.85rem;
  border: 1px solid #bcae9f;
  border-radius: 0.65rem;
  color: #2d241d;
  background: #ffffff;
}

input:focus,
select:focus {
  border-color: #b84f13;
  outline: 3px solid rgba(184, 79, 19, 0.2);
}

.operation-picker {
  padding: 0;
  border: 0;
}

.operation-picker legend {
  margin-bottom: 0.55rem;
}

.operation-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.4rem;
}

.operation-button {
  display: flex;
  min-height: 3.1rem;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.15rem;
  padding: 0.35rem 0.2rem;
  border: 1px solid #bda895;
  border-radius: 0.65rem;
  color: #49392c;
  background: #f5eadb;
  font-size: 0.72rem;
  font-weight: 650;
  line-height: 1.1;
}

.operation-button:hover:not(:disabled) {
  border-color: #a54417;
  background: #f0dbc7;
}

.operation-button.is-selected {
  border-color: #a54417;
  color: #ffffff;
  background: #a54417;
  box-shadow: inset 0 -3px rgba(69, 27, 10, 0.22);
}

.operation-symbol {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 1.25rem;
  font-weight: 400;
  line-height: 1;
}

.form-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.65rem;
}

.utility-button {
  min-height: 3.2rem;
  padding: 0.75rem 1.1rem;
  border-radius: 0.7rem;
  font-weight: 700;
}

.utility-button {
  border: 1px solid #8f7d6c;
  color: #3b3027;
  background: #fffaf2;
}

.utility-button:hover:not(:disabled) {
  background: #eee2d2;
}

.reset-button {
  border-color: #55463a;
  color: #ffffff;
  background: #55463a;
}

.reset-button:hover:not(:disabled) {
  background: #3b3027;
}

button:focus-visible,
input:focus-visible {
  outline: 3px solid rgba(184, 79, 19, 0.35);
  outline-offset: 3px;
}

button:disabled {
  cursor: wait;
  opacity: 0.65;
}

.feedback-grid {
  margin-top: 2rem;
}

.feedback-panel {
  min-height: 6.5rem;
  padding: 1rem;
  border: 1px solid transparent;
  border-radius: 0.75rem;
}

.result-panel {
  border-color: #b8c5ad;
  background: #eef3e9;
}

.result-panel.is-active {
  border-left: 0.35rem solid #4f6b42;
  box-shadow: inset 0 0 0 1px rgba(79, 107, 66, 0.08);
}

.feedback-panel output,
.feedback-panel p {
  display: block;
  margin-top: 0.55rem;
  color: #2d241d;
  font-size: 1.05rem;
}

.error-panel {
  border-color: #e2b6ae;
  background: #fff0ed;
}

.error-panel.is-active {
  border-left: 0.35rem solid #a6372c;
  box-shadow: inset 0 0 0 1px rgba(166, 55, 44, 0.08);
}

.error-panel p {
  color: #812c24;
}

@media (min-width: 36rem) {
  .number-fields,
  .feedback-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .operation-button {
    min-height: 3.2rem;
    flex-direction: row;
    gap: 0.35rem;
    padding: 0.45rem;
    font-size: 0.82rem;
  }
}
</style>
