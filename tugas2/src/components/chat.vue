<template>
  <div class="chat-container">
    <h2 style="color: white;">ChatGPT dengan API</h2>
    <div>
      <input
        type="text"
        v-model="userInput"
        placeholder="Tanyakan sesuatu..."
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">Kirim</button>
    </div>

    <div class="response">
      <p style="color:white"><strong>Respons:</strong> {{ response }}</p>
    </div>

    <div v-if="error" class="error">
      <p>Error: {{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userInput: "",
      response: "",
      error: null,
    };
  },
  methods: {
    async sendMessage() {
      if (!this.userInput) return;

      this.response = "";
      this.error = null;

      try {
        const result = await axios.post(
          "https://api.openai.com/v1/chat/completions",
          {
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: this.userInput }],
          },
          {
            headers: {
              Authorization: `Bearer`,
              "Content-Type": "application/json",
            },
          }
        );
        this.response = result.data.choices[0].text.trim();
      } catch (error) {
        this.error = "Terjadi kesalahan, coba lagi nanti.";
        if (error.response) {
          console.error("Error response:", error.response.data);
        } else if (error.request) {
          console.error("Error request:", error.request);
        } else {
          console.error("Error:", error.message);
        }
      }
    },
  },
};
</script>

<style scoped>
.chat-container {
width: 100%;
  /* max-width: 400px; */
  margin: 0 auto;
  text-align: center;
}
input {
  width: 80%;
  padding: 8px;
  margin: 8px 0;
}
button {
  padding: 8px 16px;
}
.response {
  margin-top: 20px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
