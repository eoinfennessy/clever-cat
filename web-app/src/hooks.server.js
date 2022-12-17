import PocketBase from 'pocketbase';
import { serialiseNonPojos } from '$lib/utils';

export const handle = async ({ event, resolve }) => {
    event.locals.pb = new PocketBase('http://pocketbase:8000');
    event.locals.pb.authStore.loadFromCookie(event.request.headers.get('cookie') || '');

    if (event.locals.pb.authStore.isValid) {
        event.locals.user = serialiseNonPojos(event.locals.pb.authStore.model);
    } else {
        event.locals.user = undefined;
    }

    const response = await resolve(event);

    response.headers.set('set-cookie', event.locals.pb.authStore.exportToCookie({ secure: false }));

    return response;
};
