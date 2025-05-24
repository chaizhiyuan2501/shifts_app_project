// \src\router\routes.ts
export const constantRoute = [
    {
        path: "/login",
        component: () => import("@/views/login/index.vue"),
        name: "login"
    },
    {
        path: "/guest",
        component: () => import("@/views/guest/index.vue"),
        name: "guest"
    },
    {
        path: "/staff",
        component: () => import("@/views/staff/index.vue"),
        name: "staff"
    },
    {
        path: "/meal",
        component: () => import("@/views/meal/index.vue"),
        name: "meal"
    },
    {
        path: "/",
        component: () => import("@/views/home/index.vue"),
        name: "home"
    },
    {
        path: "/404",
        component: () => import("@/views/404/index.vue"),
        name: "404"
    },
    {
        path: "/:pathMatch(.*)*",
        redirect: "/404",
        name: "Any"
    },
]