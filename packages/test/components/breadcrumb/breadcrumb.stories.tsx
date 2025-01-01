import React from 'react';
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbSeparator } from './breadcrumb';

export default {
    title: 'Components/Breadcrumb',
    component: Breadcrumb,
};

export const Default = () => (
    <Breadcrumb>
        <BreadcrumbItem>
            <BreadcrumbLink href="#">Home</BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator />
        <BreadcrumbItem>
            <BreadcrumbLink href="#">Library</BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator />
        <BreadcrumbItem>
            <BreadcrumbLink href="#">Data</BreadcrumbLink>
        </BreadcrumbItem>
    </Breadcrumb>
);
