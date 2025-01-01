import React from 'react';
import { Avatar, AvatarImage, AvatarFallback } from './avatar';

export default {
    title: 'Components/Avatar',
    component: Avatar,
};

export const Default = () => (
    <Avatar>
        <AvatarImage src="https://via.placeholder.com/150" alt="Avatar" />
        <AvatarFallback>AB</AvatarFallback>
    </Avatar>
);
