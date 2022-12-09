import { serialiseNonPojos } from '$lib/utils'
import { error } from '@sveltejs/kit'

export const load = async ({ locals, params }) => {
    if (!locals.authStore.isValid) {
        throw error(401, "Unauthenticated")
    }

    try {
        const project = serialiseNonPojos(locals.pb.collection('projects').getOne(params.projectId));

        if (locals.user.id === project.user) {
            return project
        } else {
            throw error(403, "Forbidden")
        }
    } catch (err) {
        console.log('Error: ', err);
        throw error(err.status, err.message);
    }
}