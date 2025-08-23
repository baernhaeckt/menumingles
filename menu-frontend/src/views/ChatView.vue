<script setup lang="ts">
import { getWebSocketClient } from "@/client/websocket-client";
import { type ChatMessage, ChatMessageSchema } from "@/schemas/chat-message";
import { IconFridge, IconSend, IconUser } from "@tabler/icons-vue";
import { useHead } from '@unhead/vue';

import { onMounted, onUnmounted, ref } from 'vue';
import { type ZodSafeParseResult } from "zod";

useHead({
  title: 'Chat • Menu Mingles',
  meta: [
    {
      name: 'description',
      content: 'Chat with your household members',
    },
  ],
  link: [
    {
      rel: 'icon',
    }
  ]
})

const messages = ref<ChatMessage[]>([]);
const newMessage = ref('');
const connectionStatus = ref<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');
const reconnectAttempts = ref(0);

const websocketClient = getWebSocketClient({
  serverAddress: 'wss://menu-mingles-minglers-brcebbdfb5cefdh8.northeurope-01.azurewebsites.net/api/v1/ws', // TODO: configure this somewhere?
  onMessageReceived: (message) => {
    console.log('Received message:', message.data.original);

    let parsedMessage: ZodSafeParseResult<ChatMessage>;
    if (message.data.original) {
      parsedMessage = ChatMessageSchema.safeParse(message.data.original);
    } else {
      parsedMessage = ChatMessageSchema.safeParse(JSON.parse(message.data));
    }
    if (parsedMessage.success) {
      messages.value.push(parsedMessage.data);
    }
  },
  onOpen: () => {
    console.log('WebSocket connected successfully!');
    connectionStatus.value = 'connected';
    reconnectAttempts.value = 0;
  },
  onClose: (event) => {
    console.log('WebSocket disconnected:', event.code, event.reason);
    connectionStatus.value = 'disconnected';
  },
  onError: (event) => {
    console.error('WebSocket error:', event);
    connectionStatus.value = 'error';
  },
  autoReconnect: true,
  reconnectInterval: 3000,
  maxReconnectAttempts: 15, // Increased from 5 to 15
  pingInterval: 90000, // 90 seconds
  pingTimeout: 90000 // 90 seconds
});

// Monitor reconnection attempts
const checkReconnectionStatus = () => {
  reconnectAttempts.value = websocketClient.getReconnectAttempts();
};

const sendMessage = () => {
  if (newMessage.value.trim() && connectionStatus.value === 'connected') {
    // Send message via WebSocket
    websocketClient.send(JSON.stringify(ChatMessageSchema.parse({
      name: 'User', // This could be dynamic based on user profile
      message: newMessage.value.trim(),
    })));

    newMessage.value = '';
  }
};

const handleKeyPress = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
};

onMounted(async () => {
  connectionStatus.value = 'connecting';
  try {
    await websocketClient.connect();
  } catch (error) {
    console.error('Failed to connect to WebSocket server:', error);
    connectionStatus.value = 'error';
  }

  // Set up periodic status check
  const statusInterval = setInterval(checkReconnectionStatus, 500);

  onUnmounted(() => {
    clearInterval(statusInterval);
  });
});

const manualReconnect = async () => {
  console.log('Manual reconnect initiated.');
  websocketClient.disconnect();
  connectionStatus.value = 'connecting';
  try {
    await websocketClient.connect();
  } catch (error) {
    console.error('Failed to reconnect to WebSocket server:', error);
    connectionStatus.value = 'error';
  }
};
</script>

<template>
  <div class="p-10 h-full flex flex-col grow gap-4 overflow-scroll">
    <!-- Connection Status Indicator -->
    <div class="fixed top-4 right-4 z-50">
      <div
           :class="{
            'bg-green-500': connectionStatus === 'connected',
            'bg-yellow-500': connectionStatus === 'connecting',
            'bg-red-500': connectionStatus === 'disconnected' || connectionStatus === 'error'
          }"
           class="px-3 py-1 rounded-full text-white text-sm font-medium shadow-lg">
        {{ connectionStatus === 'connected' ? 'Connected' :
          connectionStatus === 'connecting' ? 'Connecting...' :
            connectionStatus === 'disconnected' ? 'Disconnected' : 'Error' }}
        <span v-if="reconnectAttempts > 0" class="ml-2 text-xs">
          ({{ reconnectAttempts }})
        </span>
      </div>
      <!-- Manual Reconnect Button -->
      <button
              v-if="connectionStatus === 'disconnected' || connectionStatus === 'error'"
              @click="manualReconnect"
              class="mt-2 bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded-full text-white text-sm font-medium shadow-lg">
        Reconnect
      </button>
    </div>

    <!-- Messages Container -->
    <div v-if="messages.length === 0" class="flex-1 flex items-center justify-center text-neutral-500">
      <p>No messages yet. Start a conversation!</p>
    </div>

    <!-- Dynamic Messages -->
    <div
         v-for="(message, index) in messages"
         :key="index"
         :class="[
          'w-3/4',
          message.name === 'Fridge' ? '' : 'self-end'
        ]">
      <div :class="[
        'flex gap-3',
        message.name === 'Fridge' ? 'flex-row' : 'flex-row-reverse'
      ]">
        <div class="bg-neutral-300 rounded-full w-10 h-10 p-2 aspect-square">
          <IconFridge v-if="message.name === 'Fridge'" class="w-full h-full text-neutral-600" />
          <IconUser v-else class="w-full h-full text-neutral-600" />
        </div>
        <div :class="[
          'p-4 pt-3 rounded-2xl',
          message.name === 'Fridge'
            ? 'text-neutral-700 bg-neutral-300'
            : 'text-neutral-800 bg-red-200'
        ]">
          <span v-if="message.name !== 'Fridge'" class="block font-bold text-green-600">{{ message.name }}</span>
          <span v-else class="block font-bold text-blue-500">{{ message.name }}</span>
          <span>{{ message.message }}</span>
        </div>
      </div>
    </div>
  </div>
  <div class="rounded-tl-2xl rounded-tr-2xl bg-red-200 mx-4! px-5 py-4 drop-shadow-[0_-10px_40px_rgba(0,0,0,0.15)]">
    <div class="w-full flex flex-row gap-5">
      <input
             v-model="newMessage"
             @keypress="handleKeyPress"
             type="text"
             class="bg-white rounded-2xl grow px-4 outline-4 outline-transparent focus:outline-rose-600"
             placeholder="Type a message..." />
      <button
              @click="sendMessage"
              :disabled="!newMessage.trim() || connectionStatus !== 'connected'"
              class="bg-rose-600 hover:bg-rose-700 disabled:bg-gray-400 disabled:cursor-not-allowed cursor-pointer rounded-3xl px-4 aspect-square text-white">
        <IconSend />
      </button>
    </div>
  </div>
</template>

<style>
#main-sec {
  display: flex;
  flex-direction: column;
}

div#app {
  max-height: 100vh;
}
</style>
