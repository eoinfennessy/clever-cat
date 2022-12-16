<script>
    import { page } from '$app/stores';

    const navigation = [
        {
            title: 'My Feeders',
            href: '/my/dashboard/feeders'
        },
        {
            title: 'My Pets',
            href: '/my/dashboard/pets'
        },
        {
            title: 'View & Tag Photos',
            href: '/my/dashboard/photos'
        }
    ]
</script>

<div class="w-full h-full px-2">
    <h3 class="text-2xl font-medium">Dashboard</h3>
    <div class="divider"></div>
</div>
<div class="flex w-full h-full spce-x-4">
    <ul class="menu bg-base-100 w-56 p-2 rounded-box">
        {#each navigation as navItem}
            <li>
                <a href={navItem.href} class="font-medium {$page.url.pathname.includes(navItem.href) ? 'active' : ''}">{navItem.title}</a>
            </li>
        {/each}
    </ul>
    <div class="w-full">
        <slot />
    </div>
</div>