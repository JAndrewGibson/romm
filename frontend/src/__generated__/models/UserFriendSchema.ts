/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UserSchema } from './UserSchema';
import type { SimpleRomSchema } from './SimpleRomSchema';

export type UserFriendSchema = UserSchema & {
    recent_games: Array<SimpleRomSchema>;
    play_time_ms: number;
};
