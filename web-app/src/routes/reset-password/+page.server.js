import { error } from "@sveltejs/kit";

export const actions = {
  resetPassword: async ({ locals, request }) => {
    const body = Object.fromEntries(await request.formData());
    try {
      locals.pb.collection("users").requestPasswordReset(body.email);
      return {
        success: true,
      };
    } catch (err) {
      console.log("Error: ", err);
      throw error(500, "Encountered error while requesting password reset");
    }
  },
};
