<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { ROUTES } from "@/plugins/router";

withDefaults(
  defineProps<{
    block?: boolean;
    height?: string;
    rounded?: boolean;
    withTag?: boolean;
  }>(),
  {
    block: false,
    height: "",
    rounded: false,
    withTag: false,
  },
);
const { t } = useI18n();
</script>
<template>
  <v-btn
    icon
    :block="block"
    variant="flat"
    rounded="1"
    :height="height"
    class="py-4 bg-background d-flex align-center justify-center"
    :class="{ rounded: rounded }"
    :to="{ name: ROUTES.FRIENDS }"
    :color="$route.name == ROUTES.FRIENDS ? 'toplayer' : 'background'"
  >
    <div class="d-flex flex-column align-center">
      <v-icon :color="$route.name == ROUTES.FRIENDS ? 'primary' : ''">
        mdi-account-group
      </v-icon>
      <v-expand-transition>
        <span
          v-if="withTag"
          class="text-caption text-center"
          :class="{ 'text-primary': $route.name == ROUTES.FRIENDS }"
          >{{ t("common.friends") }}</span
        >
      </v-expand-transition>
    </div>
  </v-btn>
</template>
