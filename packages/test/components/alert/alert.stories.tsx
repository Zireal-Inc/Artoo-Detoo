import React from 'react';
import { Alert, AlertTitle, AlertDescription } from './alert';

export default {
    title: 'Components/Alert',
    component: Alert,
};

export const Default = () => (
    <Alert>
        <AlertTitle>Alert Title</AlertTitle>
        <AlertDescription>Alert Description</AlertDescription>
    </Alert>
);
