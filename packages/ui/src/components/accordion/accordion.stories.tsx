// import React from 'react';
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from './accordion';


export default {
    title: 'Components/Accordion',
    component: Accordion,
    // parameters: {
    //     layout: 'centered',
    // },
};

export const Simple = () => (
    <Accordion type="single" collapsible className="w-full">
        <AccordionItem value="item-1">
            <AccordionTrigger>Is it accessible?</AccordionTrigger>
            <AccordionContent>
                Yes. It adheres to the WAI-ARIA design pattern.
            </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-2">
            <AccordionTrigger>Is it styled?</AccordionTrigger>
            <AccordionContent>
                Yes. It comes with default styles that matches the other
                components&apos; aesthetic.
            </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-3">
            <AccordionTrigger>Is it animated?</AccordionTrigger>
            <AccordionContent>
                Yes. It's animated by default, but you can disable it if you prefer.
            </AccordionContent>
        </AccordionItem>
    </Accordion>
);

export const MultipleItems = () => (
    <Accordion type="multiple" className="w-full">
        <AccordionItem value="item-1">
            <AccordionTrigger>Can I open multiple items?</AccordionTrigger>
            <AccordionContent>
                Yes. You can open multiple items at the same time.
            </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-2">
            <AccordionTrigger>Is it customizable?</AccordionTrigger>
            <AccordionContent>
                Yes. You can customize the styles and behavior as needed.
            </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-3">
            <AccordionTrigger>Can I disable animation?</AccordionTrigger>
            <AccordionContent>
                Yes. You can disable the animation if you prefer.
            </AccordionContent>
        </AccordionItem>
    </Accordion>
);

export const CustomStyled = () => (
    <Accordion type="single" collapsible className="w-full bg-gray-100 p-4 rounded-lg">
        <AccordionItem value="item-1">
            <AccordionTrigger className="text-blue-500">Custom Styled Trigger</AccordionTrigger>
            <AccordionContent className="text-gray-700">
                This is a custom styled accordion item.
            </AccordionContent>
        </AccordionItem>
    </Accordion>
);
