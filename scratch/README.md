This is a thought space for how I would potentially write an end-to-end script for home brewing this application.

I'm of the conclusion that for now, it makes sense to initialize the Secrets Manager *outside* of the application stack.

This is because I cannot find a way to sanely initialize the secret without the potential for hard-coding secrets into the samconfig.toml file. If the file were to be ignored, then the user would need to provide the secrets on EVERY invocation. Which is potentially fine because they would only do it once, but not sure.