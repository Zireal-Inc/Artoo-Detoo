import { Button } from './button'
import type { Meta, StoryObj } from '@storybook/react'
import { fn } from '@storybook/test'

const meta = {
    title: 'Components/Button',
    component: Button,
    parameters: {
        layout: 'centered',
    },
    tags: ['autodocs'],
    argTypes: {},
    args: { onClick: fn() },
} satisfies Meta<typeof Button>

export default meta

type Story = StoryObj<typeof meta>

export const Primary: Story = {
    args: {
        children: 'Button',
    },
}

export const Destructive: Story = {
    args: {
        variant: 'destructive',
        children: 'Destructive Button',
    },
}

export const Outline: Story = {
    args: {
        variant: 'outline',
        children: 'Outline Button',
    },
}

export const Secondary: Story = {
    args: {
        variant: 'secondary',
        children: 'Secondary Button',
    },
}

export const Ghost: Story = {
    args: {
        variant: 'ghost',
        children: 'Ghost Button',
    },
}

export const Link: Story = {
    args: {
        variant: 'link',
        children: 'Link Button',
    },
}

export const Small: Story = {
    args: {
        size: 'sm',
        children: 'Small Button',
    },
}

export const Large: Story = {
    args: {
        size: 'lg',
        children: 'Large Button',
    },
}

export const Icon: Story = {
    args: {
        size: 'icon',
        children: '🔍',
    },
}