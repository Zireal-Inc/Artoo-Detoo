import { Preview } from '@storybook/react';
import { withThemeByClassName } from '@storybook/addon-themes';
import DocumentationTemplate from './DocumentationTemplate.mdx';
// import { Title, Subtitle, Description, Primary, Controls, Stories } from '@storybook/blocks'
// import 'tailwindcss/tailwind.css'
import '../src/index.css'

const preview: Preview = {
    parameters: {
        // actions: { argTypesRegex: '^on[A-Z].*' },
        a11y: {
            // Optional selector to inspect
            element: '#storybook-root',
            config: {
                rules: [
                    {
                        // The autocomplete rule will not run based on the CSS selector provided
                        id: 'autocomplete-valid',
                        selector: '*:not([autocomplete="nope"])',
                    },
                    {
                        // Setting the enabled option to false will disable checks for this particular rule on all stories.
                        id: 'image-alt',
                        enabled: false,
                    },
                ],
            },
            // Axe's options parameter
            options: {},
            // Optional flag to prevent the automatic check
            // manual: true,
        }, 
        controls: {
            matchers: {
                color: /(background|color)$/i,
                date: /Date$/,
            },
        },
        backgrounds: {
            values: [
                // 👇 Default values
                { name: 'Dark', value: '#000' },
                { name: 'Light', value: '#F7F9F2' },
                // 👇 Add your own
                { name: 'Maroon', value: '#400' },
            ],
            // 👇 Specify which background is shown by default
            default: 'Light',
        },
        docs: {

            page: DocumentationTemplate,
            toc: {
                contentsSelector: '.sbdocs-content',
                headingSelector: 'h1, h2, h3',
                ignoreSelector: '.docs-story h2',
                title: 'Table of Contents',
                disable: false,
                unsafeTocbotOptions: {
                    orderedList: false,
                },
            },
        },
    },
    tags: ['autodocs'],
};


/* snipped for brevity */

export const decorators = [
    withThemeByClassName({
        themes: {
            light: 'light',
            dark: 'dark',
        },
        defaultTheme: 'light',
        // attributeName: 'data-mode',
    }),
];

export default preview;

// export const tags = ["autodocs"];