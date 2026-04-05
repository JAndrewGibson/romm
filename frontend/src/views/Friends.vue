<script setup lang="ts">
import { onMounted, ref } from "vue";
import type { UserFriendSchema } from "@/__generated__";
import userApi from "@/services/api/user";
import { defaultAvatarPath, formatDuration, formatRelativeDate } from "@/utils";
import { ROUTES } from "@/plugins/router";

const friends = ref<UserFriendSchema[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const response = await userApi.fetchFriends();
    friends.value = response.data;
  } catch (error) {
    console.error("Failed to fetch friends:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <v-container fluid class="pa-6">
    <h1 class="text-h4 mb-6 font-weight-bold d-flex align-center">
      <v-icon icon="mdi-account-group" class="mr-3" color="primary" />
      Friends
    </h1>

    <v-row v-if="loading">
      <v-col v-for="i in 4" :key="i" cols="12" md="6" lg="4">
        <v-skeleton-loader type="card" />
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col v-for="friend in friends" :key="friend.id" cols="12" md="6" lg="4" xl="3">
        <v-card variant="flat" rounded="xl" class="friend-card border">
          <v-card-item>
            <template #prepend>
              <v-avatar size="64" class="mr-4 border">
                <v-img :src="friend.avatar_url || defaultAvatarPath" />
              </v-avatar>
            </template>
            <v-card-title class="text-h6 font-weight-bold">
              {{ friend.username }}
            </v-card-title>
            <v-card-subtitle>
              Joined {{ formatRelativeDate(friend.created_at) }}
            </v-card-subtitle>
          </v-card-item>

          <v-divider class="mx-4 opacity-10" />

          <v-card-text>
            <div class="d-flex align-center mb-4">
              <v-icon icon="mdi-clock-outline" size="small" class="mr-2" color="medium-emphasis" />
              <span class="text-body-2 text-medium-emphasis">
                Total Playtime: <strong>{{ formatDuration(friend.play_time_ms) }}</strong>
              </span>
            </div>

            <div class="text-subtitle-2 font-weight-bold mb-3 d-flex align-center">
              <v-icon icon="mdi-history" size="small" class="mr-2" />
              Recently Played
            </div>

            <v-row no-gutters class="ga-3 overflow-x-auto pb-2 flex-nowrap hide-scrollbar">
              <div v-for="game in friend.recent_games" :key="game.id" class="recent-game-item">
                <v-tooltip bottom>
                  <template #activator="{ props }">
                    <v-hover v-slot="{ isHovering, props: hoverProps }">
                      <v-card
                        v-bind="{ ...props, ...hoverProps }"
                        :to="{ name: ROUTES.ROM, params: { rom: game.id } }"
                        width="100"
                        variant="flat"
                        rounded="lg"
                        class="overflow-hidden position-relative"
                        :elevation="isHovering ? 8 : 0"
                      >
                        <v-img 
                          :src="game.url_cover" 
                          aspect-ratio="0.75" 
                          cover
                          class="bg-grey-darken-4"
                        >
                          <template #placeholder>
                            <v-row class="fill-height ma-0" align="center" justify="center">
                              <v-progress-circular indeterminate color="grey-lighten-5" size="20" />
                            </v-row>
                          </template>
                        </v-img>
                      </v-card>
                    </v-hover>
                  </template>
                  <span>{{ game.name }}</span>
                </v-tooltip>
              </div>
              <div v-if="!friend.recent_games.length" class="text-caption text-medium-emphasis italic py-4">
                No games played yet.
              </div>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.friend-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  background: rgba(var(--v-theme-surface), 0.7) !important;
  backdrop-filter: blur(10px);
}

.friend-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2) !important;
}

.recent-game-item {
  flex: 0 0 auto;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
