variable project_id {
    type = string
    description = "Project ID of GCP Project"
}

variable region {
    type = string
}

variable zone {
    type = string
}

variable function_name {
    type = string
    default = "function-trigger-on-gcs"
}

variable runtime {
    type = string
    description = "Runtime environment for function"
    default = "python37"
}

variable function_entry_point {
    type = string
    description = "Function to execute in deployed function"
}

variable source_dir {
    type = string
    description = "The path to the function code directory"
}

variable output_path {
    type = string
    description = "The output directory for storing archive zip file"
    default = "./tmp/function.zip"
}

variable min_instances {
    type = number
    default = 1
    description = "The minimum number of cloud function instances to have always available to reduce cold start"
}

variable max_instances {
    type = number
    default = 1
    description = "The maximum number of cloud function instances to have always available for execution"
}

variable topic_name {
    type = string
    description = "The Pubsub topic name for publishing output messages"
}

variable output_format {
    type = string
    description = "The output format of the data files to convert to. (json or csv)"
}