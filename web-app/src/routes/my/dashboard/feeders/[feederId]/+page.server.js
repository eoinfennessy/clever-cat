import { serialiseNonPojos } from "$lib/utils";
import { error } from "@sveltejs/kit";

export const load = ({ locals, params }) => {
  const getProps = async (feederId) => {
    try {
      const feeder = serialiseNonPojos(
        await locals.pb
          .collection("feeders")
          .getOne(feederId, { expand: "model, model.pets" })
      );

      const model = feeder.expand.model;
      delete feeder.expand;

      const pets = model.expand.pets;
      delete model.expand;

      const feedSchedules = serialiseNonPojos(
        await locals.pb
          .collection("feed_schedules")
          .getFullList(200, { filter: `feeder = "${feederId}"`, expand: "pet" })
      );

      const lastFeeds = [];
      for (const feedSchedule of feedSchedules) {
        const lastFeed = serialiseNonPojos(
          await locals.pb.collection("feeds").getList(1, 1, {
            filter: `pet = "${feedSchedule.pet}"`,
            sort: "-created",
            expand: "photo, pet",
          })
        );
        lastFeeds.push(lastFeed);
      }
      console.log(lastFeeds[0])

      return {
        feeder: feeder,
        model: model,
        pets: pets,
        feedSchedules: feedSchedules,
        lastFeeds: lastFeeds,
      };
    } catch (err) {
      console.log("Error: ", err);
      throw error(err.status, err.message);
    }
  };
  return getProps(params.feederId);
};
