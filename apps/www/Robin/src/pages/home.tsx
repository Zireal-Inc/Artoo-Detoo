import * as React from 'react'
import { Button } from '@ui/components/ui/button/button'

export default function Home() {
    return (
        <div className="max-w-3xl mx-auto px-4 py-16">
            {/* Hero Section */}
            <section className="space-y-6 pb-12">
                <h1 className="text-4xl font-bold tracking-tight">
                    Hey, I'm <span className="text-primary">Robin Singh</span> 👋
                </h1>
                <p className="text-xl text-muted-foreground">
                    Full Stack Developer based in India. I build modern web applications
                    with React, Node.js, and cutting-edge technologies.
                </p>
                <div className="flex gap-4">
                    <Button variant="default">
                        <a href="https://github.com/yourusername" target="_blank" rel="noopener noreferrer">
                            GitHub
                        </a>
                    </Button>
                    <Button variant="outline">
                        <a href="https://linkedin.com/in/yourusername" target="_blank" rel="noopener noreferrer">
                            LinkedIn
                        </a>
                    </Button>
                </div>
            </section>

            {/* Featured Projects */}
            <section className="space-y-6 py-12">
                <h2 className="text-2xl font-bold tracking-tight">Featured Projects</h2>
                <div className="grid gap-6">
                    {projects.map((project, index) => (
                        <div key={index} className="group rounded-lg border p-4 hover:border-primary transition-colors">
                            <h3 className="text-lg font-semibold">{project.title}</h3>
                            <p className="text-muted-foreground mt-2">{project.description}</p>
                            <div className="flex gap-2 mt-4">
                                {project.technologies.map((tech, i) => (
                                    <span key={i} className="text-xs bg-secondary px-2 py-1 rounded">
                                        {tech}
                                    </span>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Tech Stack */}
            <section className="space-y-6 py-12">
                <h2 className="text-2xl font-bold tracking-tight">Tech Stack</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {techStack.map((tech, index) => (
                        <div key={index} className="flex items-center gap-2 text-muted-foreground">
                            <span className="w-2 h-2 rounded-full bg-primary"></span>
                            {tech}
                        </div>
                    ))}
                </div>
            </section>
        </div>
    )
}

const projects = [
    {
        title: "Project One",
        description: "A modern web application built with React and Node.js",
        technologies: ["React", "Node.js", "TypeScript", "Tailwind"],
    },
    {
        title: "Project Two",
        description: "Full-stack e-commerce platform with real-time features",
        technologies: ["Next.js", "PostgreSQL", "Prisma", "tRPC"],
    },
]

const techStack = [
    "React", "TypeScript", "Node.js", "Next.js",
    "PostgreSQL", "Tailwind CSS", "Git", "Docker"
]
