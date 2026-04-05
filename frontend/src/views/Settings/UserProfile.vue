<script setup lang="ts">
import type { Emitter } from "mitt";
import { storeToRefs } from "pinia";
import { inject, ref, onMounted, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import RetroAchievements from "@/components/Settings/UserProfile/RetroAchievements.vue";
import RSection from "@/components/common/RSection.vue";
import userApi from "@/services/api/user";
import storeAuth from "@/stores/auth";
import storeUsers from "@/stores/users";
import type { Events } from "@/types/emitter";
import type { UserItem } from "@/types/user";
import type { UserStatsSchema } from "@/__generated__";
import { defaultAvatarPath, getRoleIcon, formatDuration } from "@/utils";

const { t } = useI18n();
const auth = storeAuth();
const { user } = storeToRefs(auth);
const userToEdit = ref<UserItem | null>(null);
const usersStore = storeUsers();
const imagePreviewUrl = ref<string | undefined>("");
const userStats = ref<UserStatsSchema | null>(null);
const emitter = inject<Emitter<Events>>("emitter");

function triggerFileInput() {
  const fileInput = document.getElementById("file-input");
  fileInput?.click();
}

function previewImage(event: Event) {
  const input = event.target as HTMLInputElement;
  if (!input.files) return;

  const reader = new FileReader();
  reader.onload = () => {
    imagePreviewUrl.value = reader.result?.toString();
  };
  if (input.files[0]) {
    reader.readAsDataURL(input.files[0]);
  }
}

function editUser() {
  if (!userToEdit.value) return;

  userApi
    .updateUser(userToEdit.value)
    .then(({ data }) => {
      emitter?.emit("snackbarShow", {
        msg: `User ${data.username} updated successfully`,
        icon: "mdi-check-bold",
        color: "green",
        timeout: 5000,
      });
      usersStore.update(data);
      if (data.id == auth.user?.id) {
        auth.setCurrentUser(data);
      }
    })
    .catch(({ response, message }) => {
      emitter?.emit("snackbarShow", {
        msg: `Unable to edit user: ${
          response?.data?.detail || response?.statusText || message
        }`,
        icon: "mdi-close-circle",
        color: "red",
        timeout: 5000,
      });
    });

  emitter?.emit("refreshDrawer", null);
}

onMounted(async () => {
  userToEdit.value = { ...user.value, password: "", avatar: undefined };
  if (userToEdit.value) {
    document.title = `${userToEdit.value.username} | Profile`;
    try {
      const statsResponse = await userApi.fetchUserStats(userToEdit.value.id);
      userStats.value = statsResponse.data;
    } catch (error) {
      console.error("Failed to fetch user stats:", error);
    }
  }
});

onUnmounted(() => {
  imagePreviewUrl.value = "";
});
</script>
<template>
  <template v-if="userToEdit">
    <v-row class="ma-4" no-gutters>
      <v-col>
        <v-list-item>
          <template #prepend>
            <v-hover v-slot="{ isHovering, props }">
              <v-avatar size="100" v-bind="props">
                <v-img
                  :src="
                    imagePreviewUrl ||
                    (userToEdit.avatar_url || defaultAvatarPath)
                  "
                >
                  <v-fade-transition>
                    <v-btn
                      v-if="isHovering"
                      class="d-flex translucent cursor-pointer h-100 w-100 align-center justify-center text-h4"
                      @click="triggerFileInput"
                    >
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                  </v-fade-transition>
                  <v-file-input
                    id="file-input"
                    v-model="userToEdit.avatar"
                    class="file-input text-truncate"
                    label="Avatar"
                    prepend-inner-icon="mdi-image"
                    prepend-icon=""
                    variant="outlined"
                    hide-details
                    @change="previewImage"
                  />
                </v-img>
              </v-avatar>
            </v-hover>
          </template>
          <template #title>
            <v-list-item-title class="text-h6">
              {{ userToEdit.username }}
            </v-list-item-title>
          </template>
          <template #subtitle>
            <v-list-item-subtitle class="mt-2">
              {{ userToEdit.role
              }}<v-icon class="ml-1">
                {{ getRoleIcon(userToEdit.role) }}
              </v-icon>
            </v-list-item-subtitle>
          </template>
        </v-list-item>
      </v-col>
    </v-row>

    <RSection class="ma-4" icon="mdi-account" title="Account details">
      <template #content>
        <v-text-field
          v-model="userToEdit.username"
          class="ma-4"
          variant="outlined"
          :label="t('settings.username')"
          :rules="usersStore.usernameRules"
          required
          clearable
        />
        <v-text-field
          v-model="userToEdit.password"
          class="ma-4"
          variant="outlined"
          :label="t('settings.password')"
          clearable
        />
        <v-text-field
          v-model="userToEdit.email"
          class="ma-4"
          variant="outlined"
          :label="t('settings.email')"
          :rules="usersStore.emailRules"
          required
          clearable
        />
        <v-select
          v-model="userToEdit.role"
          class="ma-4"
          variant="outlined"
          :items="['viewer', 'editor', 'admin']"
          :label="t('settings.role')"
          required
          hide-details
        >
          <template #selection="{ item }">
            <v-list-item class="pa-0">
              <v-icon class="mr-2">
                {{ getRoleIcon(item.title) }}
              </v-icon>
              {{ item.title }}
            </v-list-item>
          </template>
          <template #item="{ item }">
            <v-list-item :title="item.title">
              <template #prepend>
                <v-icon>{{ getRoleIcon(item.title) }}</v-icon>
              </template>
            </v-list-item>
          </template>
        </v-select>
        <v-btn
          :variant="!userToEdit.username ? 'plain' : 'flat'"
          :disabled="!userToEdit.username"
          class="ml-4 text-romm-green bg-toplayer"
          @click="editUser"
        >
          {{ t("common.apply") }}
        </v-btn>
      </template>
    </RSection>

    <RetroAchievements class="mx-4 mt-8" />

    <RSection v-if="userStats && userStats.top_played_roms.length" class="ma-4 mt-8" icon="mdi-chart-bar" title="Stats">
      <template #content>
        <div class="pa-4">
          <div v-for="(game, index) in userStats.top_played_roms" :key="game.id" class="mb-6">
            <div class="d-flex justify-space-between mb-1">
              <span class="text-subtitle-1 font-weight-bold">{{ game.name }}</span>
              <span class="text-subtitle-2 opacity-70">{{ formatDuration(game.play_time_ms) }}</span>
            </div>
            <div class="d-flex align-center">
              <div class="flex-grow-1 mr-4">
                <v-progress-linear
                  :model-value="(game.play_time_ms / userStats.top_played_roms[0].play_time_ms) * 100"
                  height="32"
                  rounded
                  color="primary"
                  class="stats-bar elevation-2"
                >
                  <template #default="{ value }">
                    <span class="ml-4 text-caption font-weight-black opacity-50">{{ Math.ceil(value) }}%</span>
                  </template>
                </v-progress-linear>
              </div>
              <v-avatar size="64" rounded="lg" class="elevation-4 border-sm">
                <v-img :src="game.merged_screenshots?.[0] || game.url_cover" cover />
              </v-avatar>
            </div>
          </div>
        </div>
      </template>
    </RSection>
    <RSection v-else-if="userStats" class="ma-4 mt-8" icon="mdi-chart-bar" title="Stats">
      <template #content>
        <div class="pa-8 text-center text-medium-emphasis">
          <v-icon size="x-large" class="mb-2 opacity-30">mdi-timer-off-outline</v-icon>
          <p>No playtime data available yet.</p>
        </div>
      </template>
    </RSection>
  </template>
</template>

<style scoped>
.stats-bar :deep(.v-progress-linear__background) {
  opacity: 0.1 !important;
}
.stats-bar :deep(.v-progress-linear__determinate) {
  transition: width 1s ease-in-out;
}
</style>
