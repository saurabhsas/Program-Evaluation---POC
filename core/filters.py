def apply_filters(
    df,
    gender,
    lob,
    fsproduct,
    accountid,
    accountname,
    county,
    zipcode,
    age_category
):

    if lob != "All":
        df = df[df["LINEOFBUSINESS"] == lob]

    if fsproduct != "All":
        df = df[df["FSPRODUCT"] == fsproduct]

    if accountid != "All":
        df = df[df["ACCOUNTID"] == accountid]

    if accountname != "All":
        df = df[df["ACCOUNTNAME"] == accountname]

    if county != "All":
        df = df[df["COUNTY"] == county]

    if zipcode != "All":
        df = df[df["ZIPCODE"] == zipcode]

    if age_category != "All":
        df = df[df["AGE_CATEGORY"] == age_category]

    if gender != "All":
        df = df[df["GENDER"] == gender]

    return df