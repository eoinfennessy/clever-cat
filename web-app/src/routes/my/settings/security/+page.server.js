import { error, redirect } from "@sveltejs/kit";

export const actions = {
  updatePassword: async ({ request, locals }) => {
    const body = Object.fromEntries(await request.formData());

    try {
      await locals.pb.collection("users").update(locals.user.id, body);
      locals.pb.authStore.clear();
    } catch (err) {
      console.log("Error: ", err);
      throw error(err.status, err.message);
    }

    throw redirect(303, "/login");
  },
};
