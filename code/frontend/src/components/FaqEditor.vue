<template>
  <div class="faq-editor">
    <h1>{{ isEdit ? 'Edit FAQ' : 'Add FAQ' }}</h1>
    <form @submit.prevent="handleSubmit">
      <label>
        Question:
        <input type="text" v-model="question" required>
      </label>
      <label>
        Answer:
        <textarea v-model="answer" required></textarea>
      </label>
      <button type="submit">{{ isEdit ? 'Save' : 'Add' }}</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'FaqEditor',
  props: {
    faq: Object,
    isEdit: Boolean,
  },
  data() {
    return {
      question: this.faq ? this.faq.question : '',
      answer: this.faq ? this.faq.answer : '',
    };
  },
  methods: {
    handleSubmit() {
      const faq = {
        question: this.question,
        answer: this.answer,
      };
      if (this.isEdit) {
        faq.id = this.faq.id;
        this.$emit('update', faq);
      } else {
        this.$emit('add', faq);
      }
      this.question = '';
      this.answer = '';
    },
  },
};
</script>
