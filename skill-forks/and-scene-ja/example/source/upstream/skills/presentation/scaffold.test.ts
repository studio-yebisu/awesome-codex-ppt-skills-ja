import { describe, expect, it } from 'vitest'
import {
  detectAnchors,
  isMonorepo,
  resolveScaffoldTarget,
  slugFromTitle,
  REQUIRED_DEPENDENCIES,
  type ProjectSnapshot,
} from './scaffold'

describe('detectAnchors', () => {
  it('detects no anchors in empty project', () => {
    expect(detectAnchors({ files: [] })).toEqual({
      buildSetup: false,
      sceneKit: false,
      presentationIndex: false,
    })
  })

  it('detects build setup when vite config and build script exist', () => {
    const snapshot: ProjectSnapshot = {
      files: ['package.json', 'vite.config.ts'],
      packageJson: { scripts: { build: 'tsc -b && vite build' } },
    }
    expect(detectAnchors(snapshot).buildSetup).toBe(true)
  })

  it('detects scene kit when presentation-kit contract files exist', () => {
    const snapshot: ProjectSnapshot = {
      files: [
        'src/presentation-kit/types.ts',
        'src/presentation-kit/Presentation.tsx',
        'src/presentation-kit/Stage.tsx',
      ],
    }
    expect(detectAnchors(snapshot).sceneKit).toBe(true)
  })

  it('detects presentation index when registry exports presentations array', () => {
    const snapshot: ProjectSnapshot = {
      files: ['src/presentations/index.ts'],
      presentationIndexContent: 'export const presentations: PresentationEntry[] = []',
    }
    expect(detectAnchors(snapshot).presentationIndex).toBe(true)
  })

  it('rejects presentation index file without valid registry content', () => {
    const snapshot: ProjectSnapshot = {
      files: ['src/presentations/index.ts'],
    }
    expect(detectAnchors(snapshot).presentationIndex).toBe(false)
  })

  it('detects partial scaffold — only missing anchors are false', () => {
    const snapshot: ProjectSnapshot = {
      files: ['package.json', 'vite.config.ts', 'src/presentation-kit/types.ts'],
      packageJson: { scripts: { build: 'vite build' } },
    }
    const anchors = detectAnchors(snapshot)
    expect(anchors.buildSetup).toBe(true)
    expect(anchors.sceneKit).toBe(false)
    expect(anchors.presentationIndex).toBe(false)
  })
})

describe('isMonorepo', () => {
  it('returns false for standalone project', () => {
    expect(isMonorepo({ files: ['package.json'], packageJson: {} })).toBe(false)
  })

  it('returns true when package.json has workspaces', () => {
    expect(isMonorepo({ files: [], packageJson: { workspaces: ['packages/*'] } })).toBe(true)
  })

  it('returns true when pnpm-workspace.yaml exists', () => {
    expect(isMonorepo({ files: ['pnpm-workspace.yaml'] })).toBe(true)
  })

  it('returns true when packages/ layout exists', () => {
    expect(isMonorepo({ files: ['packages/foo/package.json'] })).toBe(true)
  })

  it('returns true when apps/ layout exists', () => {
    expect(isMonorepo({ files: ['apps/web/package.json'] })).toBe(true)
  })
})

describe('resolveScaffoldTarget', () => {
  it('scaffolds at root for an empty project', () => {
    expect(resolveScaffoldTarget({ files: [] })).toBe('.')
  })

  it('scaffolds at root for an existing standalone JS app', () => {
    expect(
      resolveScaffoldTarget({ files: ['package.json', 'vite.config.ts'], packageJson: {} }),
    ).toBe('.')
  })

  it('scaffolds under presentations/ in a monorepo', () => {
    expect(resolveScaffoldTarget({ files: ['pnpm-workspace.yaml'] })).toBe('presentations')
  })

  it('scaffolds under presentation/ in a non-empty non-JS repo', () => {
    expect(resolveScaffoldTarget({ files: ['main.py', 'requirements.txt', 'README.md'] })).toBe(
      'presentation',
    )
  })
})

describe('slugFromTitle', () => {
  it('converts title to kebab-case slug', () => {
    expect(slugFromTitle('How to Use This Skill')).toBe('how-to-use-this-skill')
  })

  it('strips non-alphanumeric characters', () => {
    expect(slugFromTitle('AI & ML: The Basics!')).toBe('ai-ml-the-basics')
  })
})

describe('REQUIRED_DEPENDENCIES', () => {
  it('lists runtime and dev dependencies the scaffold must ensure', () => {
    expect(REQUIRED_DEPENDENCIES.runtime).toEqual(
      expect.arrayContaining(['react', 'react-dom', 'motion', 'lucide-react']),
    )
    expect(REQUIRED_DEPENDENCIES.dev).toEqual(
      expect.arrayContaining([
        'vite',
        '@vitejs/plugin-react',
        'typescript',
        'playwright',
      ]),
    )
  })
})
