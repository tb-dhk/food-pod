import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "the food:pod wiki",
  description: "official wiki of the food:pod project",
  themeConfig: {
    nav: [
      { text: 'home', link: '/' },
      { text: 'wiki', link: '/introduction' }, // introduction as the first page
      { text: 'github', link: 'https://github.com/tb-dhk/food-pod' }, // credits as an independent link
    ],

    sidebar: [
      { text: 'introduction', link: '/introduction' }, // introduction in the sidebar
      {
        text: 'components', // updated section title
        items: [
          { text: 'smart bin', link: '/bin' }, // new link for bin component
          { text: 'mobile app', link: '/app' }, // new link for app component
          { text: 'image recognition model', link: '/model' }, // new link for model component
        ]
      },
      { text: 'credits', link: '/credits' } // credits in the sidebar
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/tb-dhk/food-pod' } // updated github link
    ]
  },
  base: "/food-pod/"
})
