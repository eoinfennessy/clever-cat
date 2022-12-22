import { error } from "@sveltejs/kit"
import { serialiseNonPojos } from '$lib/utils'

export const load = ({ locals, params }) => {
    if (!locals.pb.authStore.isValid) {
        throw redirect(303, '/login')
    }
    
    const getPhotos = async (pageNumber) => {
        try {
            const photos = serialiseNonPojos(await locals.pb.collection('pet_photos').getList(pageNumber, 3, {filter: `user = "${locals.user.id}"`, sort: '-created', expand: 'pet'}));
            return photos
        } catch (err) {
            console.log('Error: ', err);
            throw error(err.status, err.message);
        }
    }

    return {
        pb_cookie: locals.pb.authStore.exportToCookie({ httpOnly: false }),
        photos: getPhotos(params.pageNumber)
    }
}