<template>
  <div class="faq-card">
    <div class="faq-question">{{ question }}</div>
    <div class="faq-answer">{{ answer }}</div>
    <div class="faq-controls">
      <button class="faq-edit" @click="edit">Edit</button>
      <button class="faq-delete" @click="remove">Delete</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FaqCard',
  props: {
    question: {
      type: String,
      required: true,
    },
    answer: {
      type: String,
      required: true,
    },
  },
  methods: {
    edit() {
      this.$emit('edit');
    },
    remove() {
      this.$emit('remove');
    },
  },
};
</script>
