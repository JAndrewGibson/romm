/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RomUserData } from './RomUserData';
export type RomUserUpdatePayload = {
    /**
     * Partial rom user data to update. Only provided fields will be updated.
     */
    data?: RomUserData;
    /**
     * Milliseconds to add to current play time.
     */
    add_play_time_ms?: number;
    /**
     * Set last played timestamp to now.
     */
    update_last_played?: boolean;
    /**
     * Clear the last played timestamp.
     */
    remove_last_played?: boolean;
};

