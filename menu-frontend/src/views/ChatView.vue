<script setup lang="ts">
import { getWebSocketClient } from "@/client/websocket-client";
import { type ChatMessage, ChatMessageSchema } from "@/schemas/chat-message";
import { useAuthStore } from '@/stores/auth';
import { IconFridge, IconRefresh, IconSend, IconUser } from "@tabler/icons-vue";
import { useHead } from '@unhead/vue';

import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue';
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

const authStore = useAuthStore();
const messages = ref<ChatMessage[]>([]);
const newMessage = ref('');
const connectionStatus = ref<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');
const reconnectAttempts = ref(0);
const messagesContainer = ref<HTMLElement>();

// Ensure auth store is initialized
authStore.initFromCookie();

// Computed property for current user name
const currentUserName = computed(() => {
  return authStore.username || 'User';
});

const websocketClient = getWebSocketClient({
  serverAddress: 'wss://menu-mingles-minglers-brcebbdfb5cefdh8.northeurope-01.azurewebsites.net/api/v1/ws', // TODO: configure this somewhere?
  onMessageReceived: (message) => {
    let parsedMessage: ZodSafeParseResult<ChatMessage>;
    if (message.data.type === 'echo') {
      parsedMessage = ChatMessageSchema.safeParse(message.data.message);
    } else {
      parsedMessage = ChatMessageSchema.safeParse(JSON.parse(message.data));
    }
    if (parsedMessage.success) {
      // Enhance the message with the timestamp
      parsedMessage.data.timestamp = message.timestamp;
      messages.value.push(parsedMessage.data);
      // Auto-scroll to bottom when new message arrives
      nextTick(() => {
        scrollToBottom();
      });
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
  maxReconnectAttempts: 15,
  pingInterval: 30000,
  pingTimeout: 10000
});

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const checkReconnectionStatus = () => {
  reconnectAttempts.value = websocketClient.getReconnectAttempts();
};

const sendMessage = () => {
  if (newMessage.value.trim() && connectionStatus.value === 'connected') {
    const currentUser = currentUserName.value;

    // Create the message object
    const messageData = {
      type: 'broadcast',
      data: {
      name: currentUser,
        message: newMessage.value.trim()
      }
    };

    // Send message via WebSocket
    websocketClient.send(JSON.stringify(messageData));

    // Clear the input
    newMessage.value = '';

    // Scroll to bottom after sending
    nextTick(() => {
      scrollToBottom();
    });
  }
};

const handleKeyPress = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
};

const statusInterval = ref<NodeJS.Timeout | null>(null);

onMounted(async () => {
  // Ensure auth store is initialized
  authStore.initFromCookie();

  connectionStatus.value = 'connecting';
  try {
    await websocketClient.connect();
  } catch (error) {
    console.error('Failed to connect to WebSocket server:', error);
    connectionStatus.value = 'error';
  }

  // Set up periodic status check
  statusInterval.value = setInterval(checkReconnectionStatus, 500);
});

onUnmounted(() => {
  if (statusInterval.value) {
    clearInterval(statusInterval.value);
  }
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

const formatTime = (timestamp: number | undefined) => {
  if (!timestamp) {
    return '';
  }

  const date = new Date(timestamp);
  const now = new Date();
  const isToday = date.toDateString() === now.toDateString();

  if (isToday) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } else {
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' }) + ' ' +
      date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
};

const isOwnMessage = (message: ChatMessage) => {
  const currentUser = currentUserName.value;
  const isOwn = message.name === currentUser;

  return isOwn;
};
</script>

<template>
  <div class="h-[calc(100dvh-96px)] flex flex-col bg-gradient-to-br from-slate-50 to-slate-100">
    <!-- Header -->
    <div class="flex-shrink-0 bg-white border-b border-slate-200 px-6 py-4 shadow-sm">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-semibold text-slate-800">Household Chat</h1>
          <p class="text-sm text-slate-500">Stay connected with your household</p>
        </div>

        <!-- Connection Status -->
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-2">
            <div
                 :class="{
                  'bg-green-500': connectionStatus === 'connected',
                  'bg-yellow-500': connectionStatus === 'connecting',
                  'bg-red-500': connectionStatus === 'disconnected' || connectionStatus === 'error'
                }"
                 class="w-2 h-2 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-slate-600">
              {{ connectionStatus === 'connected' ? 'Connected' :
                connectionStatus === 'connecting' ? 'Connecting...' :
                  connectionStatus === 'disconnected' ? 'Disconnected' : 'Error' }}
            </span>
          </div>

          <button
                  v-if="connectionStatus === 'disconnected' || connectionStatus === 'error'"
                  @click="manualReconnect"
                  class="flex items-center gap-1 px-3 py-1.5 bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium rounded-lg transition-colors">
            <IconRefresh class="w-4 h-4" />
            Reconnect
          </button>
        </div>
      </div>
    </div>

    <!-- Messages Container -->
    <div
         ref="messagesContainer"
         class="flex-1 overflow-y-auto px-6 py-4 space-y-4 min-h-0">
      <!-- Empty State -->
      <div v-if="messages.length === 0" class="flex items-center justify-center h-full">
        <div class="text-center">
          <div class="w-16 h-16 bg-slate-200 rounded-full flex items-center justify-center mx-auto mb-4">
            <IconFridge class="w-8 h-8 text-slate-400" />
          </div>
          <h3 class="text-lg font-medium text-slate-700 mb-2">No messages yet</h3>
          <p class="text-slate-500">Start a conversation with your household members!</p>
        </div>
      </div>

      <!-- Messages -->
      <div
           v-for="(message, index) in messages"
           :key="index"
           :class="[
            'flex mb-4',
            isOwnMessage(message) ? 'justify-end' : 'justify-start'
          ]">
        <div
             :class="[
              'flex gap-3 max-w-[75%]',
              isOwnMessage(message) ? 'flex-row-reverse' : 'flex-row'
            ]">
          <!-- Avatar -->
          <div
               :class="[
                'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-sm',
                isOwnMessage(message)
                  ? 'bg-gradient-to-br from-blue-500 to-blue-600'
                  : 'bg-gradient-to-br from-slate-200 to-slate-300'
              ]">
            <IconFridge
                        v-if="message.name === 'Fridge'"
                        class="w-5 h-5 text-white" />
            <IconUser
                      v-else
                      :class="isOwnMessage(message) ? 'text-white' : 'text-slate-600'"
                      class="w-5 h-5" />
          </div>

          <!-- Message Bubble -->
          <div class="flex flex-col min-w-0">
            <!-- Name (only for received messages) -->
            <div
                 v-if="!isOwnMessage(message)"
                 class="text-xs font-medium text-slate-600 mb-1 ml-1">
              {{ message.name }}
            </div>

            <!-- Message Content -->
            <div
                 :class="[
                  'px-4 py-3 rounded-2xl shadow-sm relative break-words',
                  isOwnMessage(message)
                    ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white'
                    : 'bg-white text-slate-800 border border-slate-200'
                ]">
              <p class="text-sm leading-relaxed pr-0 pb-3 mb-0">
                <template v-if="message.type === 'fridge'">
                  <p class="mb-2">{{ message.message }}</p>
                  <a href="/swipe"
                     class="rounded-2xl mb-2 bg-red-600 hover:bg-red-700 px-6 py-2 text-white font-bold cursor-pointer w-full flex flex-row justify-center items-center gap-2 outline-4 outline-transparent outline-solid outline-offset-2 focus-visible:outline-red-200">
                    <i class="ti ti-arrow-right"></i> Start planning now
                  </a>
                </template>
                <template v-else>
                  {{ message.message }}
                </template>
              </p>

              <!-- Timestamp inside bubble -->
              <div :class="[
                    'text-xs absolute bottom-1 right-4',
                    isOwnMessage(message) ? 'text-blue-100' : 'text-slate-400'
                  ]">
                {{ formatTime(message.timestamp) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div class="flex-shrink-0 bg-white border-t border-slate-200 px-6 py-4">
      <div class="flex items-end gap-3">
        <div class="flex-1 relative">
          <input v-model="newMessage" @keypress="handleKeyPress" type="text" :disabled="connectionStatus !== 'connected'"
                 class="w-full px-4 py-3 pr-12 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                 placeholder="Type your message..." />
        </div>

        <button @click="sendMessage" :disabled="!newMessage.trim() || connectionStatus !== 'connected'"
                class="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-slate-300 disabled:to-slate-400 disabled:cursor-not-allowed text-white rounded-2xl flex items-center justify-center transition-all shadow-lg hover:shadow-xl">
          <IconSend class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar for messages container */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}

/* Smooth scrolling */
.overflow-y-auto {
  scroll-behavior: smooth;
}

/* Ensure full height */
.h-full {
  height: 100%;
}

/* Ensure flex container takes full height */
.flex-1 {
  flex: 1 1 0%;
}

/* Prevent flex items from shrinking */
.flex-shrink-0 {
  flex-shrink: 0;
}

/* Allow flex items to shrink to minimum content size */
.min-h-0 {
  min-height: 0;
}
</style>
