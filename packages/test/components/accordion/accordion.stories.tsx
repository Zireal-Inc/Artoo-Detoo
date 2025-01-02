import React from 'react';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from './accordion';

export default {
    title: 'Components/Accordion',
    component: Accordion,
};

export const Default = () => (
    <Accordion type="multiple">
        <AccordionItem value="item-1">
            <AccordionTrigger>Item 1</AccordionTrigger>
            <AccordionContent>Content 1</AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-2">
            <AccordionTrigger>Item 2</AccordionTrigger>
            <AccordionContent>Content 2</AccordionContent>
        </AccordionItem>
    </Accordion>
);
