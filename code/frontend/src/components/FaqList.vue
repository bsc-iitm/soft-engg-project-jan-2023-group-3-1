<template>
  <div>
    <h1>FAQs</h1>
    <div v-if="faqs.length > 0">
      <div v-for="(faq, index) in faqs" :key="index">
        <faq-card :faq="faq" v-if="isAuthorized('view', faq)" />
      </div>
    </div>
    <div v-else>
      <p>No FAQs found.</p>
    </div>
    <div v-if="isAuthorized('add', null)">
      <button @click="addFaq">Add FAQ</button>
    </div>
    <faq-editor v-if="showEditor" :faq="editingFaq" @save="saveFaq" @cancel="cancelEdit" />
  </div>
</template>

<script>
import FaqCard from "./FaqCard.vue";
import FaqEditor from "./FaqEditor.vue";
import { getFaqs, createFaq, updateFaq, deleteFaq } from "../api/faq.js";

export default {
  name: "FaqList",
  components: {
    FaqCard,
    FaqEditor,
  },
  props: {
    faqs: {
      type: Array,
      required: true,
    },
    roles: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      showEditor: false,
      editingFaq: null,
    };
  },
  methods: {
    isAuthorized,
    addFaq() {
      this.editingFaq = {
        question: "",
        answer: "",
      };
      this.showEditor = true;
    },
    editFaq(faq) {
      this.editingFaq = Object.assign({}, faq);
      this.showEditor = true;
    },
    saveFaq(faq) {
      if (!faq.id) {
        createFaq(faq)
          .then(() => {
            return getFaqs();
          })
          .then((faqs) => {
            this.$emit("update:faqs", faqs);
            this.cancelEdit();
          })
          .catch((error) => {
            console.error("Error adding FAQ", error);
          });
      } else {
        updateFaq(faq)
          .then(() => {
            return getFaqs();
          })
          .then((faqs) => {
            this.$emit("update:faqs", faqs);
            this.cancelEdit();
          })
          .catch((error) => {
            console.error("Error updating FAQ", error);
          });
      }
    },
    deleteFaq(faq) {
      if (confirm("Are you sure you want to delete this FAQ?")) {
        deleteFaq(faq.id)
          .then(() => {
            return getFaqs();
          })
          .then((faqs) => {
            this.$emit("update:faqs", faqs);
          })
          .catch((error) => {
            console.error("Error deleting FAQ", error);
          });
      }
    },
    cancelEdit() {
      this.showEditor = false;
      this.editingFaq = null;
    },
  },
};
</script>

<style>
/* Add any custom styles here */
</style>
