import { Button } from './button'
import { Loader2 } from 'lucide-react'
import type { Meta , StoryObj} from '@storybook/react'
import { fn } from '@storybook/test'

const meta: Meta<typeof Button> = {
    title: 'Components/UI/Button',
    component: Button,
    parameters: {
        layout: 'centered',
    },
    tags: ['autodocs'],
    decorators: [],
    // argTypes: {
    //     variant: {
    //         options: ['primary', 'secondary'],
    //         control: { type: 'radio' },
    //     },
    // },
    args: { onClick: fn() },
}; 

export default meta

type Story = StoryObj<typeof meta>


export const Primary: Story = {
    args: {
        variant: 'default',
        children: 'Button',
    },
}

// This is an accessible story
export const Accessible: Story = {
    args: {
        
        children: 'Button',
    },
  };


export const Secondary: Story = {
    args: {
        variant: 'secondary',
        children: 'Secondary Button',
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


export const Icon: Story = {
    args: {
        size: 'icon',
        children: '🔍',
    },
}


export const WithIcon: Story = {
    args: {
        size: 'lg',
        children: '🔍 Search',
    },
}


export const ButtonLoading: Story = {
    args: {
        size: 'lg',
        children: '🔍 Search',
    },
    render: function ButtonLoading() {
        return (
            <Button disabled>
                <Loader2 className="animate-spin" />
                Please wait
            </Button>
        )
    }
}


export const asChild: Story = {
    args: {
        size: 'lg',
        children: '🔍 Search',
    },
    render: function ButtonAsChild() {
        return (
            <Button asChild>
                <a href="/login">Login</a>
            </Button>
        )
    }
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
