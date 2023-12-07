// Code generated by mockery v2.33.3. DO NOT EDIT.

package mocks

import (
	context "context"

	mock "github.com/stretchr/testify/mock"

	model "github.com/chroma/chroma-coordinator/internal/model"

	types "github.com/chroma/chroma-coordinator/internal/types"
)

// Catalog is an autogenerated mock type for the Catalog type
type Catalog struct {
	mock.Mock
}

// CreateCollection provides a mock function with given fields: ctx, collectionInfo, ts
func (_m *Catalog) CreateCollection(ctx context.Context, collectionInfo *model.CreateCollection, ts int64) (*model.Collection, error) {
	ret := _m.Called(ctx, collectionInfo, ts)

	var r0 *model.Collection
	var r1 error
	if rf, ok := ret.Get(0).(func(context.Context, *model.CreateCollection, int64) (*model.Collection, error)); ok {
		return rf(ctx, collectionInfo, ts)
	}
	if rf, ok := ret.Get(0).(func(context.Context, *model.CreateCollection, int64) *model.Collection); ok {
		r0 = rf(ctx, collectionInfo, ts)
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).(*model.Collection)
		}
	}

	if rf, ok := ret.Get(1).(func(context.Context, *model.CreateCollection, int64) error); ok {
		r1 = rf(ctx, collectionInfo, ts)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// CreateSegment provides a mock function with given fields: ctx, segmentInfo, ts
func (_m *Catalog) CreateSegment(ctx context.Context, segmentInfo *model.CreateSegment, ts int64) (*model.Segment, error) {
	ret := _m.Called(ctx, segmentInfo, ts)

	var r0 *model.Segment
	var r1 error
	if rf, ok := ret.Get(0).(func(context.Context, *model.CreateSegment, int64) (*model.Segment, error)); ok {
		return rf(ctx, segmentInfo, ts)
	}
	if rf, ok := ret.Get(0).(func(context.Context, *model.CreateSegment, int64) *model.Segment); ok {
		r0 = rf(ctx, segmentInfo, ts)
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).(*model.Segment)
		}
	}

	if rf, ok := ret.Get(1).(func(context.Context, *model.CreateSegment, int64) error); ok {
		r1 = rf(ctx, segmentInfo, ts)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// DeleteCollection provides a mock function with given fields: ctx, collectionID
func (_m *Catalog) DeleteCollection(ctx context.Context, collectionID types.UniqueID) error {
	ret := _m.Called(ctx, collectionID)

	var r0 error
	if rf, ok := ret.Get(0).(func(context.Context, types.UniqueID) error); ok {
		r0 = rf(ctx, collectionID)
	} else {
		r0 = ret.Error(0)
	}

	return r0
}

// DeleteSegment provides a mock function with given fields: ctx, segmentID
func (_m *Catalog) DeleteSegment(ctx context.Context, segmentID types.UniqueID) error {
	ret := _m.Called(ctx, segmentID)

	var r0 error
	if rf, ok := ret.Get(0).(func(context.Context, types.UniqueID) error); ok {
		r0 = rf(ctx, segmentID)
	} else {
		r0 = ret.Error(0)
	}

	return r0
}

// GetCollections provides a mock function with given fields: ctx, collectionID, collectionName, collectionTopic
func (_m *Catalog) GetCollections(ctx context.Context, collectionID types.UniqueID, collectionName *string, collectionTopic *string) ([]*model.Collection, error) {
	ret := _m.Called(ctx, collectionID, collectionName, collectionTopic)

	var r0 []*model.Collection
	var r1 error
	if rf, ok := ret.Get(0).(func(context.Context, types.UniqueID, *string, *string) ([]*model.Collection, error)); ok {
		return rf(ctx, collectionID, collectionName, collectionTopic)
	}
	if rf, ok := ret.Get(0).(func(context.Context, types.UniqueID, *string, *string) []*model.Collection); ok {
		r0 = rf(ctx, collectionID, collectionName, collectionTopic)
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).([]*model.Collection)
		}
	}

	if rf, ok := ret.Get(1).(func(context.Context, types.UniqueID, *string, *string) error); ok {
		r1 = rf(ctx, collectionID, collectionName, collectionTopic)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// GetSegments provides a mock function with given fields: ctx, segmentID, segmentType, scope, topic, collectionID, ts
func (_m *Catalog) GetSegments(ctx context.Context, segmentID types.UniqueID, segmentType *string, scope *string, topic *string, collectionID types.UniqueID, ts int64) ([]*model.Segment, error) {
	ret := _m.Called(ctx, segmentID, segmentType, scope, topic, collectionID, ts)

	var r0 []*model.Segment
	var r1 error
	if rf, ok := ret.Get(0).(func(context.Context, types.UniqueID, *string, *string, *string, types.UniqueID, int64) ([]*model.Segment, error)); ok {
		return rf(ctx, segmentID, segmentType, scope, topic, collectionID, ts)
	}
	if rf, ok := ret.Get(0).(func(context.Context, types.UniqueID, *string, *string, *string, types.UniqueID, int64) []*model.Segment); ok {
		r0 = rf(ctx, segmentID, segmentType, scope, topic, collectionID, ts)
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).([]*model.Segment)
		}
	}

	if rf, ok := ret.Get(1).(func(context.Context, types.UniqueID, *string, *string, *string, types.UniqueID, int64) error); ok {
		r1 = rf(ctx, segmentID, segmentType, scope, topic, collectionID, ts)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// ResetState provides a mock function with given fields: ctx
func (_m *Catalog) ResetState(ctx context.Context) error {
	ret := _m.Called(ctx)

	var r0 error
	if rf, ok := ret.Get(0).(func(context.Context) error); ok {
		r0 = rf(ctx)
	} else {
		r0 = ret.Error(0)
	}

	return r0
}

// UpdateCollection provides a mock function with given fields: ctx, collectionInfo, ts
func (_m *Catalog) UpdateCollection(ctx context.Context, collectionInfo *model.UpdateCollection, ts int64) (*model.Collection, error) {
	ret := _m.Called(ctx, collectionInfo, ts)

	var r0 *model.Collection
	var r1 error
	if rf, ok := ret.Get(0).(func(context.Context, *model.UpdateCollection, int64) (*model.Collection, error)); ok {
		return rf(ctx, collectionInfo, ts)
	}
	if rf, ok := ret.Get(0).(func(context.Context, *model.UpdateCollection, int64) *model.Collection); ok {
		r0 = rf(ctx, collectionInfo, ts)
	} else {
		if ret.Get(0) != nil {
			r0 = ret.Get(0).(*model.Collection)
		}
	}

	if rf, ok := ret.Get(1).(func(context.Context, *model.UpdateCollection, int64) error); ok {
		r1 = rf(ctx, collectionInfo, ts)
	} else {
		r1 = ret.Error(1)
	}

	return r0, r1
}

// NewCatalog creates a new instance of Catalog. It also registers a testing interface on the mock and a cleanup function to assert the mocks expectations.
// The first argument is typically a *testing.T value.
func NewCatalog(t interface {
	mock.TestingT
	Cleanup(func())
}) *Catalog {
	mock := &Catalog{}
	mock.Mock.Test(t)

	t.Cleanup(func() { mock.AssertExpectations(t) })

	return mock
}
