import React from 'react';
import { AspectRatio } from './aspect-ratio';

export default {
    title: 'Components/AspectRatio',
    component: AspectRatio,
};

export const Default = () => (
    <AspectRatio ratio={16 / 9}>
        <div style={{ background: 'lightgray', width: '100%', height: '100%' }}>Content</div>
    </AspectRatio>
);
