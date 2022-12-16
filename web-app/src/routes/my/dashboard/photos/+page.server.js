import { redirect } from "@sveltejs/kit"

export const load = ({ locals }) => {
    if (!locals.pb.authStore.isValid) {
        throw redirect(303, '/login')
    }

    throw redirect(303, '/my/dashboard/photos/page/1')
}
