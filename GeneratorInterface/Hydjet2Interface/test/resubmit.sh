#declare -A centjobs=(
#    ["0x2-0x4"]="crab_20161030_135501"
#    ["1x0-1x2"]="crab_20161030_135527"
#    ["10x0-10x2"]="crab_20161030_135551"
#    ["40x0-40x2"]="crab_20161030_135617"
#)

declare -A centjobs=(
    ["02-04"]="crab_20161030_135501"
    ["10-12"]="crab_20161030_135527"
    ["20-22"]="crab_20161030_135551"
    ["30-32"]="crab_20161030_135617"
)

for cent in "${!centjobs[@]}"; do
    job=${centjobs[$cent]}
    echo "$cent - $job"
    #crab resubmit -d crab_projects/${job}
done

