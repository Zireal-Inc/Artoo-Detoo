import React from 'react';
import { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent } from './card';

export default {
    title: 'Components/Card',
    component: Card,
};

export const Default = () => (
    <Card>
        <CardHeader>
            <CardTitle>Card Title</CardTitle>
            <CardDescription>Card Description</CardDescription>
        </CardHeader>
        <CardContent>Card Content</CardContent>
        <CardFooter>Card Footer</CardFooter>
    </Card>
);
